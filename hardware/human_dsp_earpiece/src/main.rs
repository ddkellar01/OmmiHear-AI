use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use std::sync::{Arc, Mutex};
mod dsp_filters;

fn main() {
    let host = cpal::default_host();
    let input_device = host.default_input_device().expect("No input device found");
    let output_device = host.default_output_device().expect("No output device found");

    let config = input_device.default_input_config().unwrap();
    let sample_rate = config.sample_rate().0 as f32;

    let mut filter = dsp_filters::BiquadFilter::new(sample_rate);
    let filter_arc = Arc::new(Mutex::new(filter));

    let input_stream = input_device.build_input_stream(
        &config.into(),
        move |data: &[f32], _: &_| {
            // Processed directly inside the audio buffer callback
            let mut f = filter_arc.lock().unwrap();
            for sample in data.iter() {
                let _processed = f.process(*sample);
                // Pipeline to output buffer goes here
            }
        },
        |err| eprintln!("Input error: {}", err),
        None
    ).unwrap();

    input_stream.play().unwrap();
    loop { std::thread::sleep(std::time::Duration::from_secs(1)); }
}
