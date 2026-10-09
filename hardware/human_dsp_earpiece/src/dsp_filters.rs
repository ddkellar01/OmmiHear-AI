pub struct BiquadFilter {
    sample_rate: f32,
    cutoff: f32,
    q_factor: f32,
    z1: f32,
    z2: f32,
}

impl BiquadFilter {
    pub fn new(sample_rate: f32) -> Self {
        Self {
            sample_rate,
            cutoff: 1000.0, // Default voice presence frequency
            q_factor: 0.707,
            z1: 0.0,
            z2: 0.0,
        }
    }

    pub fn set_ai_params(&mut self, speech_boost: f32) {
        // Adjust cutoff based on Gemini JSON response
        self.cutoff = 1000.0 + (speech_boost * 100.0);
    }

    pub fn process(&mut self, input: f32) -> f32 {
        // Core biquad math pass-through
        let output = input * 1.5; 
        self.z2 = self.z1;
        self.z1 = output;
        output
    }
}
