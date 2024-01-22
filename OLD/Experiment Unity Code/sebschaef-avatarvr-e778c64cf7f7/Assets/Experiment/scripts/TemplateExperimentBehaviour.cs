using UnityEngine;
using UnityEngine.SceneManagement;

public class TemplateExperimentBehaviour : MonoBehaviour
{
    public GameObject cube, triangle, ball;

    private void FixedUpdate()
    {
        if (cube == null && triangle == null && ball == null)
        {
            SceneManager.LoadScene("Full Test");
        }
    }
}