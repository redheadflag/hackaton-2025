import * as Location from 'expo-location';

export async function getCurrentLocation() {
    // request premission
    let {status} = await Location.requestForegroundPermissionsAsync();
    if (status !== 'granted') {
        throw new Error('Premission to access location not granted');
    }

    //get current location
    let loc = await Location.getCurrentPositionAsync({});
    return loc.coords;
}