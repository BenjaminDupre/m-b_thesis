using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;

public class HeartRateTactileBehaviour : MonoBehaviour
{
    public float maxIntensity = 0.5f;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.layer == LayerMask.NameToLayer("Hands"))
        {
            ActuatorInfo data = other.GetComponent<ActuatorInfo>();

            if (data != null)
            {
                HapticSystem.PlayPulse(Random.Range(0, maxIntensity), 100, data.location, data.userIndex, data.actuator);
            }
        }
    }

    private void OnTriggerStay(Collider other)
    {
        ActuatorInfo data = other.GetComponent<ActuatorInfo>();
        
        if (data != null)
        {
            HapticSystem.PlayPulse(Random.Range(0, maxIntensity) / 2, 100, data.location, data.userIndex, data.actuator);
        }
    }
}
