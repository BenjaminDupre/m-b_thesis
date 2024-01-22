using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ModelFader : MonoBehaviour
{
    public float alpha = 0.5f;

    private Renderer[] mRenderers;
    
    void Start()
    {
        mRenderers = GetComponentsInChildren<Renderer>();
        SetRendererAlphas(0.5f);
    }

    public void SetRendererAlphas(float alpha)
    {
        for (int i = 0; i < mRenderers.Length; i++)
        {
            for (int j = 0; j < mRenderers[i].materials.Length; j++)
            {
                Color matColor = mRenderers[i].materials[j].color;
                matColor.a = alpha;
                mRenderers[i].materials[j].color = matColor;
            }
        }
    }
}
