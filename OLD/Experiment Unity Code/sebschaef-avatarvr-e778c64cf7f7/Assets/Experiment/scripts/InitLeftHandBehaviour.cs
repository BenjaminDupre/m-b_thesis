using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class InitLeftHandBehaviour : MonoBehaviour
{
    public GameObject leftHand, eventSystem;

    private void Start()
    {
        /*eventSystem.GetComponent<LevelBehaviour>()
            .infoText
            .GetComponent<Text>()
            .text = Strings.TWIST_YOUR_LEFT_HAND;*/
    }

    void Update()
    {
        if (GameObject.Find("/IMU_hand_l") != null)
        {
            eventSystem.GetComponent<LevelBehaviour>().OnHandInitalizationDone();
            Destroy(gameObject);
        }
    }
}
