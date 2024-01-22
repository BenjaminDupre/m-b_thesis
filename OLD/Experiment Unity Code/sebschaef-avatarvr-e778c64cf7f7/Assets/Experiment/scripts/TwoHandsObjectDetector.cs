using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TwoHandsObjectDetector
{

    public static string RIGHT_HAND = "r";
    public static string LEFT_HAND = "l";

    private readonly static float BUFFER = 0.05f;

    private static TwoHandsObjectDetector instance;

    private GameObject leftObject, rightObject;
    public Transform leftPalmCenter, rightPalmCenter;

    public GameObject objectCaught;
    private Quaternion origRotation;

    public bool IsGrabbingWithBothHands()
    {
        return leftObject != null && rightObject != null && leftObject.GetInstanceID() == rightObject.GetInstanceID();
    }

    public void SetObjectCaught()
    {
        if (objectCaught == null)
        {
            origRotation = rightObject.transform.rotation;
        }

        objectCaught = rightObject;

        objectCaught.transform.SetParent(rightPalmCenter);
        objectCaught.GetComponent<Rigidbody>().isKinematic = true;
        objectCaught.transform.position = Vector3.Lerp(leftPalmCenter.transform.position, rightPalmCenter.transform.position, 0.5f);
        objectCaught.transform.rotation = calculateRotation(objectCaught.transform.rotation);
    }



    public void releaseObject()
    {
        if (objectCaught != null)
        {
            objectCaught.GetComponent<Rigidbody>().isKinematic = false;
            objectCaught.GetComponent<Rigidbody>().useGravity = true;
            objectCaught.transform.SetParent(null);

            objectCaught = null;
        }
    }

    public void SetObjectTouched(string hand, GameObject gameObject)
    {
        if (hand == RIGHT_HAND)
            rightObject = gameObject;
        else
            leftObject = gameObject;
    }


    private Quaternion calculateRotation(Quaternion currentRotation)
    {
        Vector3 yDiff = rightPalmCenter.position - leftPalmCenter.position;
        yDiff.y = 0f;

        Vector3 zDiff = rightPalmCenter.position - leftPalmCenter.position;
        zDiff.z = 0f;

        float xAngle = leftPalmCenter.rotation.eulerAngles.x + rightPalmCenter.rotation.eulerAngles.x / 2f;
        float yAngle = -1 * Vector3.SignedAngle(yDiff, Vector3.right, Vector3.up);
        float zAngle = -1 * Vector3.SignedAngle(zDiff, Vector3.right, Vector3.forward);

        Vector3 eulerAngles = new Vector3(xAngle, yAngle, zAngle);
        eulerAngles += origRotation.eulerAngles;

        currentRotation.eulerAngles = eulerAngles;
        return currentRotation;
    }


    public static TwoHandsObjectDetector GetInstance()
    {
        if (instance == null)
        {
            instance = new TwoHandsObjectDetector();
        }

        return instance;
    }
}
