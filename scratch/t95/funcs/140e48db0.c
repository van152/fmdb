__int64 __fastcall sub_140E48DB0(__int64 a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, char a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v25; // rsi
  unsigned int v26; // eax
  int v27; // ecx
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  __int64 v34; // rsi
  __int64 v35; // rsi
  __int64 v36; // rsi
  __int64 v37; // rsi
  _BYTE v39[33]; // [rsp+47h] [rbp-21h] BYREF

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 126, 1);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 127, 1);
  if ( v12[4] != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 128, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_14150F650(a1 + 24, a2) == 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 124, 2);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 129, 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 130, 1);
  if ( *(_DWORD *)(v16 + 16) != 0
    || (unsigned __int8)sub_140DB8980(a1 + 72, a2) == 0
    || (unsigned __int8)sub_140F92AB0(
                          (unsigned int)&qword_141B5FDA8,
                          (int)a1 + 80,
                          (_DWORD)a2,
                          qword_141B5FDC8,
                          (unsigned __int8)byte_141B5FC2C ^ 1u) == 0
    || (unsigned __int8)sub_140F92E30(
                          (unsigned int)&qword_141B5FDA8,
                          (int)a1 + 96,
                          (_DWORD)a2,
                          qword_141B5FDD0,
                          (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
  {
    return 0;
  }
  if ( *(unsigned __int16 *)(a4 + 1416) < 0xDCEu )
  {
    *(_QWORD *)(a1 + 104) = -1;
  }
  else if ( (unsigned __int8)sub_140F93540(
                               (unsigned int)&qword_141B5FDA8,
                               (int)a1 + 104,
                               (_DWORD)a2,
                               qword_141B5FE00,
                               (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
  {
    return 0;
  }
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 133, 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC4u )
  {
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 134, 1);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
  }
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 142, 1);
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 143, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 145, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 146, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  if ( (unsigned __int8)sub_140F80B80(a1 + 88, a2, (unsigned __int8)byte_141B5FC2C ^ 1u) == 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 131, 1);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 132, 1);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  if ( *(unsigned __int16 *)(a4 + 1416) > 0xDC1u )
  {
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 135, 1);
    if ( *(_DWORD *)(v28 + 16) == 0 )
      goto LABEL_31;
    return 0;
  }
  v39[0] = 0;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v39, 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return 0;
  v26 = v39[0] - 1;
  if ( v26 <= 0xB )
  {
    v27 = 2207;
    if ( _bittest(&v27, v26) )
      *(_BYTE *)(a1 + 135) = *(_BYTE *)(v39[0] - 1LL + 0x14187BCFCLL);
  }
LABEL_31:
  v29 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 140, 1);
  if ( *(_DWORD *)(v29 + 16) != 0 )
    return 0;
  v30 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 141, 1);
  if ( *(_DWORD *)(v30 + 16) != 0 )
    return 0;
  v31 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 136, 1);
  if ( *(_DWORD *)(v31 + 16) != 0 )
    return 0;
  v32 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 137, 1);
  if ( *(_DWORD *)(v32 + 16) != 0 )
    return 0;
  v33 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 138, 1);
  if ( *(_DWORD *)(v33 + 16) != 0 )
    return 0;
  v34 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 147, 1);
  if ( *(_DWORD *)(v34 + 16) != 0 )
    return 0;
  v35 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 144, 1);
  if ( *(_DWORD *)(v35 + 16) != 0 )
    return 0;
  v36 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 120, 4);
  if ( *(_DWORD *)(v36 + 16) != 0 )
    return 0;
  v37 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 139, 1);
  if ( *(_DWORD *)(v37 + 16) != 0 || (unsigned __int8)sub_140DB8980(a1 + 76, a2) == 0 )
    return 0;
  return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
