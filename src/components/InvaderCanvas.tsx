'use client';

import { useEffect, useRef } from 'react';

const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
const INVADER_PATTERNS = [
  [0,0,1,0,0,1,0,0, 0,0,0,1,1,0,0,0, 0,0,1,1,1,1,0,0, 0,1,1,0,0,1,1,0, 1,1,1,1,1,1,1,1, 1,0,1,1,1,1,0,1, 1,0,1,0,0,1,0,1, 0,0,0,1,1,0,0,0],
  [0,0,0,1,1,0,0,0, 0,0,1,1,1,1,0,0, 0,1,1,1,1,1,1,0, 1,1,0,1,1,0,1,1, 1,1,1,1,1,1,1,1, 0,0,1,0,0,1,0,0, 0,1,0,1,1,0,1,0, 1,0,1,0,0,1,0,1],
  [0,0,1,0,0,1,0,0, 0,0,0,1,1,0,0,0, 0,1,1,1,1,1,1,0, 1,1,0,1,1,0,1,1, 1,1,1,1,1,1,1,1, 0,1,1,1,1,1,1,0, 0,0,1,0,0,1,0,0, 0,1,0,0,0,0,1,0],
];

const ACCENT = '#e8a830';
const TEXT = '#c8c0b0';

class MiniInvader {
  x: number;
  y: number;
  char: string;
  pattern: number[];
  speed: number;
  wobble: number;
  wobbleSpeed: number;
  size: number;
  opacity: number;
  alive: boolean;
  ch: number;

  constructor(cw: number, ch: number) {
    this.x = Math.random() * cw;
    this.y = -20;
    this.char = CHARS[Math.floor(Math.random() * CHARS.length)];
    this.pattern = INVADER_PATTERNS[Math.floor(Math.random() * 3)];
    // 15% faster than prototype base speed
    this.speed = (0.15 + Math.random() * 0.25) * 1.15;
    this.wobble = Math.random() * Math.PI * 2;
    this.wobbleSpeed = 0.005 + Math.random() * 0.008;
    this.size = 14 + Math.floor(Math.random() * 8);
    this.opacity = 0.25 + Math.random() * 0.35;
    this.alive = true;
    this.ch = ch;
  }

  update() {
    this.y += this.speed;
    this.wobble += this.wobbleSpeed;
    this.x += Math.sin(this.wobble) * 0.3;
    if (this.y > this.ch + 30) this.alive = false;
  }

  draw(ctx: CanvasRenderingContext2D) {
    ctx.save();
    ctx.globalAlpha = this.opacity;
    const px = this.size / 8;
    const ox = this.x - this.size / 2;
    const oy = this.y - this.size / 2;
    for (let i = 0; i < 64; i++) {
      if (this.pattern[i]) {
        ctx.fillStyle = ACCENT;
        ctx.fillRect(ox + (i % 8) * px, oy + Math.floor(i / 8) * px, px - 0.5, px - 0.5);
      }
    }
    ctx.globalAlpha = Math.min(1, this.opacity + 0.2);
    ctx.fillStyle = TEXT;
    ctx.font = `900 ${this.size * 0.5}px 'Courier New', monospace`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.strokeStyle = 'rgba(0,0,0,0.6)';
    ctx.lineWidth = 1.5;
    ctx.strokeText(this.char, this.x, this.y);
    ctx.fillText(this.char, this.x, this.y);
    ctx.restore();
  }
}

export default function InvaderCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Retina support
    const w = canvas.offsetWidth;
    const h = canvas.offsetHeight;
    canvas.width = w * 2;
    canvas.height = h * 2;
    ctx.scale(2, 2);

    let invaders: MiniInvader[] = [];
    let lastSpawn = 0;
    let animId: number;

    // Mobile: reduce spawn rate
    const spawnRate = w < 400 ? 2000 : 1200;

    function animate(now: number) {
      ctx!.clearRect(0, 0, w, h);

      // Spawn
      if (now - lastSpawn > spawnRate) {
        invaders.push(new MiniInvader(w, h));
        lastSpawn = now;
      }

      // Update & draw
      for (const inv of invaders) {
        inv.update();
        inv.draw(ctx!);
      }
      invaders = invaders.filter((inv) => inv.alive);

      animId = requestAnimationFrame(animate);
    }

    animId = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animId);
    };
  }, []);

  return <canvas ref={canvasRef} />;
}
