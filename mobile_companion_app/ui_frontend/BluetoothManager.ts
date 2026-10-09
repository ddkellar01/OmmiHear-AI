import { BleManager, Device } from 'react-native-ble-plx';
import { Buffer } from 'buffer';

const manager = new BleManager();
const COLLAR_SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b";
const COLLAR_CHAR_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8";

export const connectToCollar = async (): Promise<Device | null> => {
  return new Promise((resolve, reject) => {
    manager.startDeviceScan(null, null, async (error, device) => {
      if (error) return reject(error);
      if (device?.name === 'OmniHear-DogCollar') {
        manager.stopDeviceScan();
        try {
          const connectedDevice = await device.connect();
          await connectedDevice.discoverAllServicesAndCharacteristics();
          resolve(connectedDevice);
        } catch (e) {
          reject(e);
        }
      }
    });
  });
};

export const sendHapticCommand = async (device: Device, payload: any) => {
  const jsonStr = JSON.stringify(payload);
  const base64Payload = Buffer.from(jsonStr).toString('base64');
  await device.writeCharacteristicWithResponseForService(
    COLLAR_SERVICE_UUID,
    COLLAR_CHAR_UUID,
    base64Payload
  );
};
