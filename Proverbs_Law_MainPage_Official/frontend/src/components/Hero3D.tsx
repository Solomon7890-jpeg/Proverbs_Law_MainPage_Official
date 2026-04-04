"use client";

import React, { useRef, useMemo } from "react";
import { Canvas, useFrame, RootState } from "@react-three/fiber";
import { Points, PointMaterial, OrbitControls, Float } from "@react-three/drei";
import * as THREE from "three";

// Stable Harmonic Particle Generator (Moved outside to satisfy React Purity)
const generatePositions = (count: number) => {
  const pos = new Float32Array(count * 3);
  const orig = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);
    const r = 2.5 + Math.random() * 0.5;
    
    const x = r * Math.sin(phi) * Math.cos(theta);
    const y = r * Math.sin(phi) * Math.sin(theta);
    const z = r * Math.cos(phi);
    
    pos[i * 3] = x;
    pos[i * 3 + 1] = y;
    pos[i * 3 + 2] = z;

    orig[i * 3] = x;
    orig[i * 3 + 1] = y;
    orig[i * 3 + 2] = z;
  }
  return { positions: pos, originalPositions: orig };
};

function BrainParticles() {
  const ref = useRef<THREE.Points>(null!);
  const count = 3000;
  
  // Memoize the stable positions to prevent re-generation on re-render
  const { positions, originalPositions } = useMemo(() => generatePositions(count), [count]);

  useFrame((state: RootState) => {
    const time = state.clock.getElapsedTime();
    
    // Global rotation for the "Collective Intelligence"
    if (ref.current) {
        ref.current.rotation.y = time * 0.05;
        
        // Harmonic Wave Sequencing Logic
        const positionsArray = ref.current.geometry.attributes.position.array as Float32Array;
        for (let i = 0; i < count; i++) {
          const x = originalPositions[i * 3];
          const y = originalPositions[i * 3 + 1];
          const z = originalPositions[i * 3 + 2];
          
          const dist = Math.sqrt(x * x + y * y + z * z);
          const wave = Math.sin(dist * 2.0 - time * 2.5) * 0.2;
          
          positionsArray[i * 3] = x + (x / dist) * wave;
          positionsArray[i * 3 + 1] = y + (y / dist) * wave;
          positionsArray[i * 3 + 2] = z + (z / dist) * wave;
        }
        
        ref.current.geometry.attributes.position.needsUpdate = true;
        
        const scale = 1 + Math.sin(time * 0.5) * 0.03;
        ref.current.scale.set(scale, scale, scale);
    }
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
