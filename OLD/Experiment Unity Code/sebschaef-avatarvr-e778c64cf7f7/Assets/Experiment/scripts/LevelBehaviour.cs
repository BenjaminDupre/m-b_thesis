using System;
using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;
using UnityEngine.UI;
using Random = UnityEngine.Random;

public class LevelBehaviour : MonoBehaviour
{
    [Header("Levels")]
    public int experimentLevelCount = 90;
    public int trainingLevelCount = 15;

    [Header("Training")]
    public bool isTraining = false;

    [Header("Logging")]
    public string logRootDirectory = "C:/Participants/";
    public bool isLoggingEnabled = true;

    [Header("Testing")]
    public bool isStartingImmediately = false;

    [Header("Template Display GameObjects")]
    public GameObject templateCanvas;
    public GameObject infoText;
    public GameObject infoTextCanvas;
    public GameObject backgroundCanvas;

    [Header("Template Display Parameters")]
    public int gridSize = 6 * 3;
    public float timeUntilStart = 2f;
    public float timeToShow = 3f;
    public float startingTextTime = 5f;
    public GameObject template;

    [Header("Hand Positioning Parameters")]
    public float timeToWaitForBallSpawn = 1f;
    public float timeUntilCalibration = 1.5f;
    public float readyDistanceToGhostAvatar = 0.03f;
    public float grabbingHandRotationOffset = 90f;

    [Header("Hand Positioning GameObjects")]
    public GameObject tutorialGrabBall;
    public GameObject tutorialCalibrate;
    public GameObject leftWristSphere, rightWristSphere;
    public GameObject leftHandStatic, rightHandStatic;
    public GameObject leftHandTexture, rightHandTexture;
    public GameObject leftSphere, rightSphere;

    [Header("Template Display Prefabs")]
    public GameObject ballRed;
    public GameObject[] randomBalls;

    [Header("Statistics Display GameObjects")]
    public GameObject timer;
    public GameObject counter;

    [Header("Statistics Display Parameters")]
    public float timerStartTimeInSeconds = 120f;

    [Header("Button")]
    public GameObject button;

    [HideInInspector] public GameObject leftHand, rightHand;
    private GameObject grabTutorialLeftHand, grabTutorialRightHand;
    private GameObject calibrateTutorialLeftHand, calibrateTutorialRightHand;

    private int currBallPositionInTemplate = -1;

    private bool isTimerRunnning = false;
    private float time;

    [HideInInspector] public int correctCounter = 0;
    [HideInInspector] public int levelCounter = 0;

    [HideInInspector] public bool isCalibrationBlocked = false;
    [HideInInspector] public CalibrationState calibrationState = CalibrationState.ACTIVE_NOT_TRIGGERED;
    public enum CalibrationState { NOT_ACTIVE, ACTIVE_NOT_TRIGGERED, ACTIVE_TRIGGERED };

    [HideInInspector] public GrabbingState grabbingState = GrabbingState.BEFORE_TEMPLATE_IS_ACTIVE;
    public enum GrabbingState { BEFORE_TEMPLATE_IS_ACTIVE, TEMPLATE_IS_ACTIVE, AFTER_TEMPLATE_IS_ACTIVE };

    private bool isFirstCalibration = true;

    private Log log;

    private void Start()
    {
        grabTutorialLeftHand = tutorialGrabBall.transform.GetChild(0).gameObject;
        grabTutorialRightHand = tutorialGrabBall.transform.GetChild(1).gameObject;

        calibrateTutorialLeftHand = tutorialCalibrate.transform.GetChild(0).gameObject;
        calibrateTutorialRightHand = tutorialCalibrate.transform.GetChild(1).gameObject;

        time = timerStartTimeInSeconds;

        //GameObject.Find("Time").GetComponent<Text>().text = Strings.TIME;
        //GameObject.Find("Score").GetComponent<Text>().text = Strings.SCORE;

        if (isLoggingEnabled && !isTraining)
        {
            log = GetComponent<Log>();
            log.Init(logRootDirectory);
            log.StartFullLogging();
        }
    }

    // Update once per frame
    void Update()
    {
        UpdateKeyInput();
        UpdateHandsGameobjects();
        UpdateTutorials();
        UpdateStatistics();
        UpdateStatisticsUI();
    }

    private void UpdateKeyInput()
    {
        if (Input.GetKeyDown(KeyCode.R))
        {
            RestartLevel();
        }
        if (Input.GetKeyDown(KeyCode.T))
        {
            FreshStart();
        }
        if (Input.GetKeyDown(KeyCode.Z))
        {
            OnLevelFinished();
        }
        if (Input.GetKeyDown(KeyCode.F))
        {
            ForceCalibrate();
        }
        if (Input.GetKeyDown(KeyCode.B))
        {
            tutorialGrabBall.SetActive(false);
            template.GetComponent<Renderer>().enabled = true;
            SpawnBall();
        }
    }

    private void UpdateHandsGameobjects()
    {
        if (leftHand == null)
        {
            leftHand = GameObject.Find("IMU_hand_l");
        }
        else
        {
            leftHandStatic.SetActive(!isFirstCalibration);
            leftWristSphere.SetActive(isFirstCalibration);
        }


        if (rightHand == null)
        {
            rightHand = GameObject.Find("IMU_hand_r");
        }
        else
        {
            rightHandStatic.SetActive(!isFirstCalibration);
            rightWristSphere.SetActive(isFirstCalibration);
        }
    }

    private void UpdateTutorials()
    {
        if (isCalibrationBlocked && !AreHandsReadyForCalibrating())
            isCalibrationBlocked = false;

        if (!isCalibrationBlocked 
            && calibrationState == CalibrationState.ACTIVE_NOT_TRIGGERED 
            && AreHandsReadyForCalibrating())
        {
            Invoke("Calibrate", timeUntilCalibration);
            calibrationState = CalibrationState.ACTIVE_TRIGGERED;
        }


        Color textureColor = Color.black;
        // Let it flash red/black when active, but not triggered yet. Switching each second.
        if (calibrationState == CalibrationState.ACTIVE_NOT_TRIGGERED && ((int)Time.time) % 2 == 0)
            textureColor = Color.red;
        else if(calibrationState == CalibrationState.ACTIVE_TRIGGERED)
            textureColor = Color.yellow;

        leftHandTexture.GetComponent<Image>().color = textureColor;
        rightHandTexture.GetComponent<Image>().color = textureColor;

        if (AreHandsReadyForGrabbing())
        {
            if (grabbingState == GrabbingState.BEFORE_TEMPLATE_IS_ACTIVE)
            {
                infoText.GetComponent<Text>().text = Strings.HOLD_THE_POSITION;
                Invoke("CreateNewTemplate", timeUntilStart);
                grabbingState = GrabbingState.TEMPLATE_IS_ACTIVE;
            }
            else if (grabbingState == GrabbingState.AFTER_TEMPLATE_IS_ACTIVE)
            {
                tutorialGrabBall.SetActive(false);
                template.GetComponent<Renderer>().enabled = true;
                SpawnBall();
            }
        }
    }

    private void UpdateStatistics()
    {
        if (isTimerRunnning)
        {
            time -= Time.deltaTime;

            if (time <= 0)
            {
                time = 0;
                QuitExperiment();
            }
        }

        if ((isTraining && levelCounter > trainingLevelCount) || 
            GetComponent<BallSpawnController>().GetJohanneLeftBallsSum() <= 0)
        {
            QuitExperiment();
        }
    }

    private void UpdateStatisticsUI()
    {
        int minutes = (int)(time / 60f);
        int seconds = (int)(time % 60f);
        string secondsString = (seconds < 10) ? "0" + seconds : seconds.ToString();

        timer.GetComponent<Text>().text = minutes + ":" + secondsString;
        counter.GetComponent<Text>().text = levelCounter.ToString();
    }


    // Events
    public void OnHandInitalizationDone()
    {
        if (isStartingImmediately)
            RestartLevel();
    }

    public void OnBallPlacedCorrectly()
    {
        template.GetComponent<Renderer>().enabled = false;
        correctCounter++;
        levelCounter++;
    }

    public void OnBallPlacedWrong()
    {
        template.GetComponent<Renderer>().enabled = false;
        levelCounter++;
    }

    public void OnBallDropped()
    {
        template.GetComponent<Renderer>().enabled = false;
        GetComponent<BallSpawnController>().ResetJohanneSpawn();
        RestartLevel();
    }

    public void OnLevelFinished()
    {
        RestartLevel();
    }

    private void OnCalibrationFinished()
    {
        calibrationState = CalibrationState.NOT_ACTIVE;

        HapticSystem.PlayPulse(0.25f, 100, NDAPIWrapperSpace.Location.LOC_RIGHT_HAND);
        HapticSystem.PlayPulse(0.25f, 100, NDAPIWrapperSpace.Location.LOC_LEFT_HAND);

        if (isFirstCalibration)
        {
            isFirstCalibration = false;
            leftSphere.SetActive(false);
            rightSphere.SetActive(false);
            OnHandInitalizationDone();
        }
        else
        {
            infoText.GetComponent<Text>().text = Strings.IMITATE_THE_GRABBING_POSE;
            tutorialGrabBall.SetActive(true);
            grabbingState = GrabbingState.BEFORE_TEMPLATE_IS_ACTIVE;
        }
    }


    // Game state
    private void FreshStart()
    {
        infoText.SetActive(true);
        Invoke("HideStartingText", startingTextTime);
        Invoke("RestartLevel", startingTextTime);
        Invoke("RestartTimer", startingTextTime);
    }

    private void RestartLevel()
    {
        Debug.Log(
            "Stage: " + levelCounter + 
            "\nCorrect: " + correctCounter + 
            "\nTime left: " + time / 60f + 
            " minutes\nLogging alive: " + log.levelThread.IsAlive
        );

        button.GetComponent<ButtonBehaviour>().hasBeenPressed = false;
        infoText.GetComponent<Text>().text = Strings.LIE_YOUR_HANDS_ON_THE_TABLE;

        calibrationState = CalibrationState.ACTIVE_NOT_TRIGGERED;
        GetComponent<BallSpawnController>().RollNextJohanneLevel();

        /*
         * If the hand wrists are already positioned correctly
         * it is most likely that the person still kept them
         * there, but in the grabbing position.
         * We block the calibration until they move it away first.
         */
        if (AreHandsReadyForCalibrating())
            isCalibrationBlocked = true;

        StartTimer();
    }

    private void CreateNewTemplate()
    {
        infoTextCanvas.SetActive(false);
        // Removing all previous children
        foreach (Transform child in templateCanvas.transform)
        {
            Destroy(child.gameObject);
        }

        // Place all random balls first
        for (int i=0; i < gridSize - 1; i++)
        {
            GameObject randomPrefab = randomBalls[Random.Range(0, randomBalls.Length)];
            GameObject instantiatedBall = Instantiate(randomPrefab, templateCanvas.transform);
            instantiatedBall.transform.SetSiblingIndex(i);
        }

        // Place the red ball at a random child index
        GameObject redBall = Instantiate(ballRed, templateCanvas.transform);

        Vector2Int randomCoordinatesInDirection = new Vector2Int(Random.Range(0, 2), Random.Range(0, 3));
        currBallPositionInTemplate = randomCoordinatesInDirection.y * 6 + randomCoordinatesInDirection.x;
        switch (GetComponent<BallSpawnController>().direction)
        {
            case BallSpawnController.Direction.CENTER:
                currBallPositionInTemplate += 2;
                break;
            case BallSpawnController.Direction.RIGHT:
                currBallPositionInTemplate += 4;
                break;
        }
        redBall.transform.SetSiblingIndex(currBallPositionInTemplate);

        backgroundCanvas.GetComponent<Canvas>().enabled = true;
        templateCanvas.GetComponent<Canvas>().enabled = true;
        Invoke("HideCanvas", timeToShow);
    }


    // Template Canvas
    private void HideCanvas()
    {
        backgroundCanvas.GetComponent<Canvas>().enabled = false;
        templateCanvas.GetComponent<Canvas>().enabled = false;
        infoTextCanvas.SetActive(true);
        infoText.GetComponent<Text>().text = Strings.PLACE_THE_BALL;
        grabbingState = GrabbingState.AFTER_TEMPLATE_IS_ACTIVE;
    }

    private void HideStartingText()
    {
        infoText.SetActive(false);
    }


    // Tutorials: Ghost hands for grabbing and calibration
    private bool AreHandsReadyForGrabbing()
    {
        if (!tutorialGrabBall.activeSelf)
        {
            return false;
        }

        float leftHandDistance = Vector3.Distance(leftHand.transform.position, grabTutorialLeftHand.transform.position);
        float rightHandDistance = Vector3.Distance(rightHand.transform.position, grabTutorialRightHand.transform.position);

        float leftHandRotation = leftHand.transform.rotation.eulerAngles.z;
        float rightHandRotation = rightHand.transform.rotation.eulerAngles.z;

        float minRotation = 180f - grabbingHandRotationOffset;
        float maxRotation = 180f + grabbingHandRotationOffset;

        return leftHandDistance < readyDistanceToGhostAvatar 
            && rightHandDistance < readyDistanceToGhostAvatar
            && leftHandRotation >= minRotation && leftHandRotation <= maxRotation
            && rightHandRotation >= minRotation && rightHandRotation <= maxRotation;
    }

    private bool AreHandsReadyForCalibrating()
    {
        if (calibrationState == CalibrationState.NOT_ACTIVE)
        {
            return false;
        }

        float leftHandDistance = 10000f;
        float rightHandDistance = 10000f;

        leftHandDistance = Vector3.Distance(leftWristSphere.transform.position, calibrateTutorialLeftHand.transform.position);
        rightHandDistance = Vector3.Distance(rightWristSphere.transform.position, calibrateTutorialRightHand.transform.position);

        return leftHandDistance < readyDistanceToGhostAvatar && rightHandDistance < readyDistanceToGhostAvatar;
    }

    private void Calibrate()
    {
        if (!AreHandsReadyForCalibrating())
        {
            calibrationState = CalibrationState.ACTIVE_NOT_TRIGGERED;
            return;
        }

        rightHand.GetComponentInChildren<HandModelController>().Recalibrate(true);
        leftHand.GetComponentInChildren<HandModelController>().Recalibrate(true);

        OnCalibrationFinished();
    }

    private void ForceCalibrate()
    {
        rightHand.GetComponentInChildren<HandModelController>().Recalibrate(true);
        leftHand.GetComponentInChildren<HandModelController>().Recalibrate(true);

        HapticSystem.PlayPulse(0.2f, 100, NDAPIWrapperSpace.Location.LOC_RIGHT_HAND);
        HapticSystem.PlayPulse(0.2f, 100, NDAPIWrapperSpace.Location.LOC_LEFT_HAND);
    }


    // Red Ball
    private void SpawnBall()
    {
        GetComponent<BallSpawnController>().SpawnJohanneBall();
    }


    // Timer 
    private void RestartTimer()
    {
        time = timerStartTimeInSeconds;
        isTimerRunnning = true;
    }

    private void PauseTimer()
    {
        isTimerRunnning = false;
    }

    private void StartTimer()
    {
        isTimerRunnning = true;
    }


    // getter
    public int GetCurrentBallPosition()
    {
        return currBallPositionInTemplate;
    }

    
    // Quit
    private void QuitExperiment()
    {
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
}
