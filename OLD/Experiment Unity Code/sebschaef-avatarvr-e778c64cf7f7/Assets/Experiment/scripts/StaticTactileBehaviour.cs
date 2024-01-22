using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;

public class StaticTactileBehaviour : MonoBehaviour
{
    public float intensity = 0.5f;

    private void OnTriggerEnter(Collider other)
    {
        if (other.gameObject.layer == LayerMask.NameToLayer("Hands"))
        {
            ActuatorInfo data = other.GetComponent<ActuatorInfo>();

            if (data != null)
            {
                HapticSystem.PlayPulse(intensity, 100, data.location, data.userIndex, data.actuator);
            }
        }
    }

    private void OnTriggerStay(Collider other)
    {
        ActuatorInfo data = other.GetComponent<ActuatorInfo>();
        
        if (data != null)
        {
            HapticSystem.PlayPulse(intensity / 2, 100, data.location, data.userIndex, data.actuator);
        }
    }
}
