using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InitRightHandBehaviour : MonoBehaviour
{
    public GameObject leftHandTutorial;
    
    // Update is called once per frame
    void Update()
    {
        if (GameObject.Find("/IMU_hand_r") != null)
        {
            Destroy(gameObject);
            leftHandTutorial.SetActive(true);
        }
    }
}
