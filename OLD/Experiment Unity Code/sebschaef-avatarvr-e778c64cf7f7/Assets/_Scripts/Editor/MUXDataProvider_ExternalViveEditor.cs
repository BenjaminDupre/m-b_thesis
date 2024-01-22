/******************************************************************************
* Copyright © NeuroDigital Technologies, S.L. 2018							  *
* Licensed under the Apache License, Version 2.0 (the "License");			  *
* you may not use this file except in compliance with the License.			  *
* You may obtain a copy of the License at 									  *
* http://www.apache.org/licenses/LICENSE-2.0								  *
* Unless required by applicable law or agreed to in writing, software		  *
* distributed under the License is distributed on an "AS IS" BASIS,			  *
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.	  *
* See the License for the specific language governing permissions and		  *
* limitations under the License.										      *
*******************************************************************************/

using UnityEngine;
using UnityEditor;
using System.Collections.Generic;
using System.Linq;

[CustomEditor(typeof(MUXDataProvider_ExternalVive))]
public class MUXDataProvider_ExternalViveEditor : MUXDataProvider_ExternalEditor
{
    private static GUIStyle ToggleButtonStyleNormal = null;
    private static GUIStyle ToggleButtonStyleToggled = null;

    SerializedProperty _positionSource;
    SerializedProperty _rotationSource;

    MUXDataProvider_ExternalVive muxDataProviderVive;

    /// <summary>
    /// Symbols that will be added to the editor
    /// </summary>
    public static readonly string[] Symbols = new string[] {
        "VIVE_TRACKERS"
    };

    /// <summary>
    /// Add define symbols as soon as Unity gets done compiling.
    /// </summary>
    static void AddDefineSymbols()
    {
        string definesString = PlayerSettings.GetScriptingDefineSymbolsForGroup(EditorUserBuildSettings.selectedBuildTargetGroup);
        List<string> allDefines = definesString.Split(';').ToList();
        allDefines.AddRange(Symbols.Except(allDefines));
        PlayerSettings.SetScriptingDefineSymbolsForGroup(
            EditorUserBuildSettings.selectedBuildTargetGroup,
            string.Join(";", allDefines.ToArray()));
    }

    private void OnEnable()
    {
        AddDefineSymbols();
    }

    public override void OnInspectorGUI()
    {
        muxDataProviderVive = (MUXDataProvider_ExternalVive)target;

        serializedObject.Update();
        EditorGUI.BeginChangeCheck();

        if (muxDataProviderVive.positionSource == null)
            muxDataProviderVive.positionSource = muxDataProviderVive.transform;

        if (muxDataProviderVive.rotationSource == null)
            muxDataProviderVive.rotationSource = muxDataProviderVive.transform;

        if (muxDataProviderVive.priorityPositiveValue < 0)
            muxDataProviderVive.priorityPositiveValue = 0;

        muxDataProviderVive.priorityPositiveValue = EditorGUILayout.IntField("Priority Value", muxDataProviderVive.priorityPositiveValue);

        GUILayout.Space(10);

        EditorGUILayout.LabelField("Positions", EditorStyles.boldLabel);

        GUILayout.BeginHorizontal();

        muxDataProviderVive.bonesToControlPosition[0] = EditorGUILayout.Toggle(SensorID.Hand.ToString(), muxDataProviderVive.bonesToControlPosition[0]);

        muxDataProviderVive.bonesToControlPositionType[0] = (Type_MUXValueType)EditorGUILayout.EnumPopup(muxDataProviderVive.bonesToControlPositionType[0]);

        _positionSource = serializedObject.FindProperty("positionSource");
        EditorGUILayout.PropertyField(_positionSource, GUIContent.none);

        GUILayout.EndHorizontal();

        muxDataProviderVive.positionOffset = EditorGUILayout.Vector3Field("Position offset", muxDataProviderVive.positionOffset);

        GUILayout.Space(10);

        EditorGUILayout.LabelField("Rotations", EditorStyles.boldLabel);

        GUILayout.BeginHorizontal();

        SensorID enumDisplayStatus = SensorID.Hand;
        muxDataProviderVive.bonesToControlRotation[(int)SensorID.Hand] = EditorGUILayout.Toggle(enumDisplayStatus.ToString(), muxDataProviderVive.bonesToControlRotation[(int)SensorID.Hand]);

        muxDataProviderVive.bonesToControlRotationType[(int)SensorID.Hand] = (Type_MUXValueType)EditorGUILayout.EnumPopup(muxDataProviderVive.bonesToControlRotationType[(int)SensorID.Hand]);

        _rotationSource = serializedObject.FindProperty("rotationSource");
        EditorGUILayout.PropertyField(_rotationSource, GUIContent.none);

        GUILayout.EndHorizontal();

        muxDataProviderVive.rotationOffset = EditorGUILayout.Vector3Field("Rotation offset", muxDataProviderVive.rotationOffset);

        if (EditorGUI.EndChangeCheck())
        {
            serializedObject.ApplyModifiedProperties();
        }

        if (Application.isPlaying)
        {
            if (ToggleButtonStyleNormal == null)
            {
                ToggleButtonStyleNormal = "Button";
                ToggleButtonStyleToggled = new GUIStyle(ToggleButtonStyleNormal);
                ToggleButtonStyleToggled.normal.background = ToggleButtonStyleToggled.active.background;
            }

            GUILayout.BeginHorizontal();

            if (GUILayout.Button("Enabled", isActive ? ToggleButtonStyleToggled : ToggleButtonStyleNormal))
            {
                isActive = true;
                muxDataProviderVive.SetActive(isActive);
            }

            if (GUILayout.Button("Disabled", !isActive ? ToggleButtonStyleToggled : ToggleButtonStyleNormal))
            {
                isActive = false;
                muxDataProviderVive.SetActive(isActive);
            }

            GUILayout.EndHorizontal();

            muxDataProviderVive.SetActive(isActive);
        }
    }
}