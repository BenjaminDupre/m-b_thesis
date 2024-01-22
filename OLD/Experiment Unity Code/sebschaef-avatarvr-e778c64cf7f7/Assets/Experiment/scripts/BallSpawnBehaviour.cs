using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BallSpawnBehaviour : MonoBehaviour
{
    public bool isGestureSpawnEnabled = false;

    // The gesture to perform to initiate the spawn process
    public Gesture initialGesture;

    // The time which has to pass after the gesture until the actual ball is being spawned (in seconds)
    public float spawnTimeAfterGesture = 2f;

    // The negative and positive angle threshold of the hand rotation relative to 180°
    public float handRotationThreshold = 20f;

    // The offset vector specifying the spawn position relative to the hand's palm center
    public Vector3 ballSpawnPositionOffset = new Vector3(0, 0.1f, 0); 

    // Ball prefabs
    public Transform redBall;

    public Transform palmCenter;

    public float timeToReenableGrabbingDetection = 2f;

    private bool isGesture = false;
    private bool wasGestureAndUpsideDown = false;
    private bool isHandUpsideDown = false;

    private float minAngle, maxAngle;
    private float passedTime = 0f;

    private HandModelController hmc;
    private IEnumerator coroutine;

    private void Awake()
    {
        hmc = GetComponent<HandModelController>();

        minAngle = 300f - handRotationThreshold;
        maxAngle = 300f + handRotationThreshold;
    }

    void Start()
    {
        coroutine = GetDevice();
        StartCoroutine(coroutine);
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.B))
        {
            //SpawnBall();
        }


        if (isGestureSpawnEnabled)
        {
            float currentHandRotationX = transform.eulerAngles.x;
            isHandUpsideDown = currentHandRotationX <= maxAngle && currentHandRotationX >= minAngle;

            if (wasGestureAndUpsideDown && !isGesture)
            {
                // Gesture is finished -> Starting the timer
                passedTime += Time.deltaTime;
                wasGestureAndUpsideDown = false;
            }
            else if (passedTime > 0)
            {
                // incrementing the timer and eventually spawning the ball or resetting everything
                passedTime += Time.deltaTime;

                if (passedTime >= spawnTimeAfterGesture)
                {
                    if (isHandUpsideDown)
                        SpawnBall();
                    else
                        Reset();
                }
            }
            else
            {
                wasGestureAndUpsideDown = isGesture && isHandUpsideDown;
                isGesture = false;
            }
        }
    }

    private IEnumerator GetDevice()
    {
        while (hmc.device == null)
        {
            yield return new WaitForSeconds(0.5f);
            if (hmc.device != null)
            {
                switch (initialGesture)
                {
                    case Gesture.IndexPinchGesture:
                        hmc.device.isPinchGestureEvent += new NDDevice.isPinchGestureHandler(SetIsGesture);
                        break;
                    case Gesture.MiddlePinchGesture:
                        hmc.device.isMiddlePinchGestureEvent += new NDDevice.isMiddlePinchGestureHandler(SetIsGesture);
                        break;
                    case Gesture.GunGesture:
                        hmc.device.isGunGestureEvent += new NDDevice.isGunGestureHandler(SetIsGesture);
                        break;
                    case Gesture.OkGesture:
                        hmc.device.isOkGestureEvent += new NDDevice.isOkGestureHandler(SetIsGesture);
                        break;
                    case Gesture.ThreePinchGesture:
                        hmc.device.isThreePinchGestureEvent += new NDDevice.isThreePinchGestureHandler(SetIsGesture);
                        break;
                    case Gesture.PinchFistGesture:
                        hmc.device.isPinchFistGestureEvent += new NDDevice.isPinchFistGestureHandler(SetIsGesture);
                        break;
                }
            }
        }
    }

    public void SetIsGesture()
    {
        isGesture = true;
    }

    private void Reset()
    {
        isGesture = false;
        wasGestureAndUpsideDown = false;
        isHandUpsideDown = false;
        passedTime = 0f;
    }

    public void SpawnBall()
    {
        ObjectDetector objectDetector = GetComponent<ObjectDetector>();
        objectDetector.isDetectionEnabled = false;

        Transform ballTransform = Instantiate(redBall, transform.position + ballSpawnPositionOffset, Quaternion.identity);
        GameObject ballGameObject = ballTransform.gameObject;

        objectDetector.objectCaught = ballGameObject;
        ballGameObject.transform.SetParent(palmCenter);
        ballGameObject.GetComponent<Rigidbody>().isKinematic = true;
        ballGameObject.transform.localPosition = new Vector3(0f, 0f, -ballGameObject.GetComponent<Collider>().bounds.extents.z);

        Invoke("ReenableGrabbingDetection", timeToReenableGrabbingDetection);

        Reset();
    }

    private void ReenableGrabbingDetection()
    {
        GetComponent<ObjectDetector>().isDetectionEnabled = true;
    }
}
