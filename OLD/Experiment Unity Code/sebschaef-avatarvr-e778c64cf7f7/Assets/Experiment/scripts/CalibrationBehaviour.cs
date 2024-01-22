using System;
using System.Collections;
using System.Collections.Generic;
using UnityDLL.Core;
using UnityDLL.Haptic;
using UnityEngine;
using UnityEngine.UI;

public class CalibrationBehaviour : MonoBehaviour
{
    public int layerMask = 1 << 10;
    public GameObject rightHand;
    public GameObject leftHand;
    public GameObject calibrationCube;

    public float watchDuration = 2f;

    public float confirmationIntensity = 0.5f;
    public int confirmationDuration = 100;

    private float watchTimer = 0;

    // Start is called before the first frame update
    void Start()
    {
        layerMask = LayerMask.GetMask("Calibration");
        //GameObject.Find("Calibration Text").GetComponent<Text>().text = String.Format(Strings.CALIBRATION_LOOK_AT_ME, (int) watchDuration);
    }

    // Update is called once per frame
    void Update()
    {
        RaycastHit hit;
        if (Physics.Raycast(transform.position, transform.TransformDirection(Vector3.forward), out hit, Mathf.Infinity, layerMask))
        {
            watchTimer += Time.deltaTime;
            calibrationCube.GetComponent<Renderer>().material.color = Color.red;
            Debug.DrawRay(transform.position, transform.TransformDirection(Vector3.forward) * 100f, Color.red);
        }
        else
        {
            watchTimer = 0;
            calibrationCube.GetComponent<Renderer>().material.color = Color.white;
            Debug.DrawRay(transform.position, transform.TransformDirection(Vector3.forward) * 100f, Color.white);
        }

        if (watchTimer > watchDuration)
        {
            calibrate();
            HapticSystem.PlayPulse(confirmationIntensity, confirmationDuration);
            watchTimer = 0;
        }
    }

    void calibrate()
    {
        rightHand.GetComponent<HandModelController>().Recalibrate(true);
        leftHand.GetComponent<HandModelController>().Recalibrate(true);
        resetAllGrabbableObjects();
    }

    void resetAllGrabbableObjects()
    {
        int grabbableLayer = LayerMask.GetMask("Grabbable");
        GameObject[] gameObjects = FindObjectsOfType<GameObject>();

        foreach (GameObject gameObject in gameObjects)
        {
            if (gameObject.layer == grabbableLayer)
            {
                gameObject.GetComponent<Rigidbody>().isKinematic = false;
                gameObject.GetComponent<Rigidbody>().useGravity = true;
                gameObject.transform.parent = null;
            }
        }
    }
}
