/// <reference types="@react-three/fiber" />
declare module '@react-three/fiber';
declare module '@react-three/drei';
declare module 'three';

// Add explicit JSX types for three.js elements to fix TS errors in Home.tsx
import { MeshProps, GroupProps, CylinderGeometryProps, BoxGeometryProps, MeshStandardMaterialProps, AmbientLightProps, DirectionalLightProps } from '@react-three/fiber';
declare global {
	namespace JSX {
		interface IntrinsicElements {
			mesh: MeshProps;
			group: GroupProps;
			cylinderGeometry: CylinderGeometryProps;
			boxGeometry: BoxGeometryProps;
			meshStandardMaterial: MeshStandardMaterialProps;
			ambientLight: AmbientLightProps;
			directionalLight: DirectionalLightProps;
		}
	}
}
