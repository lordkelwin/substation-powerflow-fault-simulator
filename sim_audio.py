"""
sim_audio.py
Procedural Web Audio API sound synthesizer for EE 415 3D Substation Simulator.
Zero external audio files required!
"""

def get_js_audio():
    return """
    class SubstationAudioEngine {
      constructor() {
        this.ctx = null;
        this.enabled = false;
        this.humOsc1 = null;
        this.humOsc2 = null;
        this.humGain = null;
      }

      init() {
        if (this.ctx) return;
        try {
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          this.ctx = new AudioContext();
          this.enabled = true;
          this.startTransformerHum();
        } catch (e) {
          console.warn("Web Audio not supported or blocked", e);
        }
      }

      startTransformerHum() {
        if (!this.ctx || this.humOsc1) return;
        // 60 Hz fundamental + 120 Hz magnetostriction harmonic
        this.humOsc1 = this.ctx.createOscillator();
        this.humOsc1.type = 'sawtooth';
        this.humOsc1.frequency.setValueAtTime(60, this.ctx.currentTime);

        this.humOsc2 = this.ctx.createOscillator();
        this.humOsc2.type = 'sine';
        this.humOsc2.frequency.setValueAtTime(120, this.ctx.currentTime);

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(150, this.ctx.currentTime);

        this.humGain = this.ctx.createGain();
        this.humGain.gain.setValueAtTime(0.04, this.ctx.currentTime);

        this.humOsc1.connect(filter);
        this.humOsc2.connect(filter);
        filter.connect(this.humGain);
        this.humGain.connect(this.ctx.destination);

        this.humOsc1.start();
        this.humOsc2.start();
      }

      stopTransformerHum() {
        if (this.humGain && this.ctx) {
          this.humGain.gain.setTargetAtTime(0, this.ctx.currentTime, 0.1);
        }
      }

      resumeTransformerHum() {
        if (this.humGain && this.ctx) {
          this.humGain.gain.setTargetAtTime(0.04, this.ctx.currentTime, 0.1);
        }
      }

      playBreakerTrip() {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        // Mechanical spring clunk + metallic latch snap
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.15);

        gain.gain.setValueAtTime(0.8, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.25);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);

        // Noise burst for mechanical latch
        this.playNoiseBurst(0.12, 0.4);
      }

      playDisconnectOperate() {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        // Motor gear hum for 1.5 seconds
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(240, now);
        osc.frequency.linearRampToValueAtTime(260, now + 1.2);

        gain.gain.setValueAtTime(0.15, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 1.4);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 1.4);
      }

      playLightning() {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        // Immediate high-voltage snap followed by low-frequency rolling thunder
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(450, now);
        osc.frequency.exponentialRampToValueAtTime(40, now + 0.6);

        gain.gain.setValueAtTime(1.0, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 1.2);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 1.2);

        this.playNoiseBurst(0.8, 0.9);
      }

      playArcFlashBlast() {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        // Violent low-frequency explosion + electric hiss
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.exponentialRampToValueAtTime(25, now + 0.8);

        gain.gain.setValueAtTime(1.0, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 1.0);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 1.0);

        this.playNoiseBurst(1.0, 1.0);
        this.playSiren(3); // 3-second emergency evacuation siren
      }

      playNoiseBurst(duration, volume) {
        if (!this.ctx) return;
        const bufferSize = this.ctx.sampleRate * duration;
        const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
        const data = buffer.getChannelData(0);
        for (let i = 0; i < bufferSize; i++) {
          data[i] = Math.random() * 2 - 1;
        }

        const noise = this.ctx.createBufferSource();
        noise.buffer = buffer;

        const filter = this.ctx.createBiquadFilter();
        filter.type = 'bandpass';
        filter.frequency.setValueAtTime(800, this.ctx.currentTime);
        filter.Q.setValueAtTime(1.5, this.ctx.currentTime);

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(volume, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(this.ctx.destination);

        noise.start();
      }

      playSiren(durationSeconds) {
        if (!this.ctx) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';

        // Modulate frequency between 600 Hz and 950 Hz
        for (let t = 0; t < durationSeconds; t += 0.5) {
          osc.frequency.setValueAtTime(600, now + t);
          osc.frequency.linearRampToValueAtTime(950, now + t + 0.25);
          osc.frequency.linearRampToValueAtTime(600, now + t + 0.5);
        }

        gain.gain.setValueAtTime(0.3, now);
        gain.gain.setValueAtTime(0.3, now + durationSeconds - 0.2);
        gain.gain.linearRampToValueAtTime(0.0, now + durationSeconds);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + durationSeconds);
      }

      playGravelFootstep() {
        if (!this.ctx) return;
        this.playNoiseBurst(0.06, 0.08);
      }

      playGeigerClick() {
        if (!this.ctx || !this.enabled) return;
        const now = this.ctx.currentTime;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(3200, now);
        osc.frequency.exponentialRampToValueAtTime(800, now + 0.012);

        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.015);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.015);
      }

      playCoronaHum() {
        if (!this.ctx || !this.enabled) return;
        const now = this.ctx.currentTime;
        // Buzzing 120 Hz / 240 Hz discharge tone + high frequency arc crackle
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(120, now);
        osc.frequency.setValueAtTime(240, now + 0.08);

        gain.gain.setValueAtTime(0.35, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);

        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start(now);
        osc.stop(now + 0.18);

        this.playNoiseBurst(0.12, 0.3);
      }
    }

    const soundEngine = new SubstationAudioEngine();
    """
