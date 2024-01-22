using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;

public class TemplateObjectBehaviour : MonoBehaviour
{

    public Collider templateCollider;
    public GameObject explosion;

    public float intensity = 0.5f;
    public int duration = 100;

    private void OnCollisionEnter(Collision collision)
    {
        if (collision.collider == templateCollider)
        {
            HapticSystem.PlayPulse(intensity, duration);
            Instantiate(explosion, this.transform.position, Quaternion.identity);
            Destroy(gameObject);
        }
    }
}
