"use client";

import React, { useRef, useMemo } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import { Points, PointMaterial, OrbitControls, Float } from "@react-three/drei";
import * as THREE from "three";

function BrainParticles() {
  const ref = useRef<THREE.Points>(null!);
  
  // Create a sphere of particles representing the "Ultimate Brain"
  const count = 2000;
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);
      const r = 2 + Math.random() * 0.5; // Radius with slight variation
      
      pos[i * 3] = r * Math.sin(phi) * Math.cos(theta);
      pos[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
      pos[i * 3 + 2] = r * Math.cos(phi);
    }
    return pos;
  }, []);

  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    
    // Pulsing and slow rotation
    ref.current.rotation.y = time * 0.1;
    ref.current.rotation.z = time * 0.05;
    
    // Subtle scale pulsing like a "Heartbeat" of intelligence
    const scale = 1 + Math.sin(time * 0.5) * 0.05;
    ref.current.scale.set(scale, scale, scale);
  });

  return (
    <group rotation={[0, 0, Math.PI / 4]}>
      <Points ref={ref} positions={positions} stride={3} frustumCulled={false}>
        <PointMaterial
          transparent
          color="#eab308" // Gold
          size={0.05}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      
      {/* Inner core glow */}
      <mesh>
        <sphereGeometry args={[1.5, 32, 32]} />
        <meshBasicMaterial color="#1e3a8a" transparent opacity={0.1} />
      </mesh>
    </group>
  );
}

export default function Hero3D() {
  return (
    <div className="absolute inset-0 z-0 h-full w-full opacity-60">
      <Canvas camera={{ position: [0, 0, 10], fov: 45 }}>
        <color attach="background" args={["#09090b"]} />
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} intensity={1} color="#eab308" />
        
        <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
          <BrainParticles />
        </Float>
        
        <OrbitControls 
          enableZoom={false} 
          enablePan={false} 
          autoRotate 
          autoRotateSpeed={0.5} 
        />
      </Canvas>
    </div>
  );
}
