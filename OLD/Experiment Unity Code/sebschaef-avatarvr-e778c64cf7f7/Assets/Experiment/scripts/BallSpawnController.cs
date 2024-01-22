using System.Collections;
using System.Collections.Generic;
using UnityDLL.Haptic;
using UnityEngine;

public class BallSpawnController : MonoBehaviour
{
    public GameObject rightHand, leftHand, rightHandPalmCenter, leftHandPalmCenter;

    [Header("Pulse paramaters")]
    public float pulseIntensity = 0.2f;
    public int pulseDuration = 100;

    public enum Hand { LEFT, RIGHT };
    public Hand hand = Hand.LEFT;

    public enum FeedbackType { NONE, CONGRUENT, INCONGRUENT };
    public FeedbackType feedbackType = FeedbackType.NONE;

    public enum Direction { LEFT, CENTER, RIGHT };
    public Direction direction = Direction.LEFT;

    [Header("Stage parameters")]
    public int stageSize = 15;
    public int johanneStageSize = 5;

    private int linearStagesBallsSpawned = 0;

    private int[] randomStagesBallsSpawned = new int[] { 0, 0, 0, 0, 0, 0 };
    private int lastSpawnIndex = -1;

    private int[][][] johanneBallsSpawned = new int[][][] {
        new int[][] {
            new int[] { 0, 0, 0 },
            new int[] { 0, 0, 0 },
            new int[] { 0, 0, 0 }
        },
        new int[][] {
            new int[] { 0, 0, 0 },
            new int[] { 0, 0, 0 },
            new int[] { 0, 0, 0 }
        },
    };
    private Vector3Int lastSpawnIndices = Vector3Int.zero;

    public bool isLeftHandVibrating = false;
    public bool isRightHandVibrating = false;

    /*private void Start()
    {
        for (int i = 0; i < 90; i++)
            RollNextJohanneLevel();

        string output = "{ ";
        for (int i = 0; i < johanneBallsSpawned.Length; i++)
        {
            output += "{ ";
            for (int j = 0; j < johanneBallsSpawned[i].Length; j++)
            {
                output += "{ ";
                for (int k = 0; k < johanneBallsSpawned[i][j].Length; k++)
                {
                    output += johanneBallsSpawned[i][j][k] + ", ";
                }
                output += " }";
            }
            output += " }";
        }
        output += " }";

        Debug.Log(output);
    }*/

    void Update()
    {
        // No vibrational feedback with the spawned ball
        if (Input.GetKeyDown(KeyCode.B))
        {
            SpawnInRandomHand();
            feedbackType = FeedbackType.NONE;
        }
        // Vibrational feedback in the same hand
        else if (Input.GetKeyDown(KeyCode.N))
        {
            SpawnInRandomHand();
            feedbackType = FeedbackType.CONGRUENT;
        }
        // Vibrational feedback in the other hand
        else if (Input.GetKeyDown(KeyCode.M))
        {
            SpawnInRandomHand();
            feedbackType = FeedbackType.INCONGRUENT;
        }

        isLeftHandVibrating = false;
        isRightHandVibrating = false;
        if (feedbackType == FeedbackType.CONGRUENT)
        {
            if (rightHandPalmCenter.transform.childCount > 1)
            {
                HapticSystem.PlayPulse(pulseIntensity, pulseDuration, NDAPIWrapperSpace.Location.LOC_RIGHT_HAND);
                isRightHandVibrating = true;
            }
            else if (leftHandPalmCenter.transform.childCount > 1)
            {
                HapticSystem.PlayPulse(pulseIntensity, pulseDuration, NDAPIWrapperSpace.Location.LOC_LEFT_HAND);
                isLeftHandVibrating = true;
            }
        }
        else if (feedbackType == FeedbackType.INCONGRUENT)
        {
            if (rightHandPalmCenter.transform.childCount > 1)
            {
                HapticSystem.PlayPulse(pulseIntensity, pulseDuration, NDAPIWrapperSpace.Location.LOC_LEFT_HAND);
                isLeftHandVibrating = true;
            }
            else if (leftHandPalmCenter.transform.childCount > 1)
            {
                HapticSystem.PlayPulse(pulseIntensity, pulseDuration, NDAPIWrapperSpace.Location.LOC_RIGHT_HAND);
                isRightHandVibrating = true;
            }
        }
    }

    private void SpawnInRandomHand()
    {
        int randomHand = Random.Range(0, 2);

        if (randomHand == 0)
            rightHand.GetComponent<BallSpawnBehaviour>().SpawnBall();
        else
            leftHand.GetComponent<BallSpawnBehaviour>().SpawnBall();
    }


    /*
     * Spawns 90 Balls linear in stages:
     *  - 15 left match
     *  - 15 right match
     *  - 15 left mismatch
     *  - 15 right mismatch
     *  - 15 left non stimulated
     *  - 15 right non stimulated
     */
    public void LinearStagesBallSpawn()
    {
        if (linearStagesBallsSpawned < stageSize * 2)
            feedbackType = FeedbackType.CONGRUENT;
        else if (linearStagesBallsSpawned < stageSize * 4)
            feedbackType = FeedbackType.INCONGRUENT;
        else // < stageSize * 6
            feedbackType = FeedbackType.NONE;

        if (linearStagesBallsSpawned < stageSize ||
            (linearStagesBallsSpawned >= stageSize * 2 && linearStagesBallsSpawned < stageSize * 3) ||
            (linearStagesBallsSpawned >= stageSize * 4 && linearStagesBallsSpawned < stageSize * 5))
            leftHand.GetComponent<BallSpawnBehaviour>().SpawnBall();
        else
            rightHand.GetComponent<BallSpawnBehaviour>().SpawnBall();

        linearStagesBallsSpawned++;
    }

    public void ResetLinearSpawn()
    {
        linearStagesBallsSpawned--;
    }


    /*
     * Spawns 90 Balls randomly, but 15 times of each stage:
     *  - 15 left congruent: 0 (counter position in array)
     *  - 15 right congruent: 1
     *  - 15 left incongruent: 2
     *  - 15 right incongruent: 3
     *  - 15 left none: 4
     *  - 15 right none: 5
     */
    public void RandomStagesBallSpawn()
    {
        int randomVal = Random.Range(0, GetRandomStagesLeftBallsSum());

        int totalStageCount = 0;
        for (int i = 0; i < randomStagesBallsSpawned.Length; i++)
        {
            totalStageCount += stageSize - randomStagesBallsSpawned[i];
            if (randomVal < totalStageCount)
            {
                /*
                 * Picking and setting the feedback + hand combination based
                 * on the stage (i)
                 */

                if (i == 0 || i == 1)
                    feedbackType = FeedbackType.CONGRUENT;
                else if (i == 2 || i == 3)
                    feedbackType = FeedbackType.INCONGRUENT;
                else
                    feedbackType = FeedbackType.NONE;


                if (i % 2 == 0)
                    leftHand.GetComponent<BallSpawnBehaviour>().SpawnBall();
                else
                    rightHand.GetComponent<BallSpawnBehaviour>().SpawnBall();

                randomStagesBallsSpawned[i]++;
                lastSpawnIndex = i;
                break;
            }
        }
    }

    public int GetRandomStagesLeftBallsSum()
    {
        int sum = 0;

        foreach (int count in randomStagesBallsSpawned)
            sum += stageSize - count;

        return sum;
    }

    public void ResetRandomSpawn()
    {
        randomStagesBallsSpawned[lastSpawnIndex]--;
    }


    /*
     * Spawns 90 Balls randomly 
     * -> 45 times each side 
     * -> 15 times each feedback
     * -> 5 times each direction (left, center, right) in the template:
     * 
     * - left hand
     * -- congruent
     * --- left
     * --- center
     * --- right
     * -- incongruent
     * --- left
     * --- center
     * --- right
     * -- none
     * --- left
     * --- center
     * --- right
     * - right hand
     * -- congruent
     * --- left
     * --- ...
     * 
     * See also GetJohanneLeftBallsSum() for the array structure
     */
    public void RollNextJohanneLevel()
    {
        int randomVal = Random.Range(0, GetJohanneLeftBallsSum());

        int totalStageCount = 0;
        for (int i = 0; i < johanneBallsSpawned.Length; i++)
        {
            for (int j = 0; j < johanneBallsSpawned[i].Length; j++)
            {
                for (int k = 0; k < johanneBallsSpawned[i][j].Length; k++)
                {
                    totalStageCount += johanneStageSize - johanneBallsSpawned[i][j][k];

                    if (randomVal < totalStageCount)
                    {
                        switch (i)
                        {
                            case 0:
                                hand = Hand.LEFT;
                                break;
                            default:
                                hand = Hand.RIGHT;
                                break;
                        }

                        switch (j)
                        {
                            case 0:
                                feedbackType = FeedbackType.CONGRUENT;
                                break;
                            case 1:
                                feedbackType = FeedbackType.INCONGRUENT;
                                break;
                            default:
                                feedbackType = FeedbackType.NONE;
                                break;
                        }

                        switch (k)
                        {
                            case 0:
                                direction = Direction.LEFT;
                                break;
                            case 1:
                                direction = Direction.CENTER;
                                break;
                            default:
                                direction = Direction.RIGHT;
                                break;
                        }

                        lastSpawnIndices = new Vector3Int(i, j, k);
                        return;
                    }
                }
            }
        }
    }

    public int GetJohanneLeftBallsSum()
    {
        int sum = 0;

        foreach (int[][] handCount in johanneBallsSpawned)
            foreach (int[] feedbackCount in handCount)
                foreach (int directionCount in feedbackCount)
                    sum += johanneStageSize - directionCount;

        return sum;
    }

    public void ResetJohanneSpawn()
    {
        johanneBallsSpawned[lastSpawnIndices.x][lastSpawnIndices.y][lastSpawnIndices.z]--;
    }

    public void SpawnJohanneBall()
    {
        if (hand == Hand.LEFT)
            leftHand.GetComponent<BallSpawnBehaviour>().SpawnBall();
        else
            rightHand.GetComponent<BallSpawnBehaviour>().SpawnBall();

        johanneBallsSpawned[lastSpawnIndices.x][lastSpawnIndices.y][lastSpawnIndices.z]++;
    }
}
