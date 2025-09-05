import pyvjoy

class FPVJoystick:
    def __init__(self, device_id=1):
        try:
            self.j = pyvjoy.VJoyDevice(device_id)
        except pyvjoy.vJoyException as e:
            raise RuntimeError(f"Failed to initialize vJoy device {device_id}: {e}")

    @staticmethod
    def _scale(value):
        value = max(0.0, min(1.0, value))
        return int(value * 32767)

    def set_axis(self, roll=0.5, pitch=0.5, yaw=0.5, throttle=0.5):
        self.j.set_axis(pyvjoy.HID_USAGE_X, self._scale(roll))
        self.j.set_axis(pyvjoy.HID_USAGE_Y, self._scale(pitch))
        self.j.set_axis(pyvjoy.HID_USAGE_Z, self._scale(yaw))
        self.j.set_axis(pyvjoy.HID_USAGE_RX, self._scale(throttle))

    def set_switch(self, switch, state=True):
        if switch < 1 or switch > 4:
            raise ValueError("Switch must be 1–4")
        self.j.set_button(switch, int(state))

    def reset(self):
        self.set_axis(0.5, 0.5, 0.5, 0.5)
        for btn in range(1, 5):
            self.set_switch(btn, False)

if __name__ == "__main__":
    js = FPVJoystick()

    import time
    try:
        while True:
            js.set_axis(roll=0.5, pitch=1.0, yaw=0.25, throttle=0.75)
            js.set_switch(1, True)
            time.sleep(1)
            js.set_switch(1, False)
            time.sleep(1)
    except KeyboardInterrupt:
        js.reset()
        print("Joystick reset and exiting.")