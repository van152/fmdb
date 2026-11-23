__int64 __fastcall sub_1411A1280(__int64 a1, _QWORD *a2, unsigned int a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v12; // rsi
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
  unsigned __int64 i; // r15
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  __int64 v27; // rsi
  __int64 v28; // rsi
  __int64 v29; // rsi
  __int64 v30; // rsi
  __int64 v31; // rsi
  __int64 v32; // rsi
  __int64 v33; // rsi
  unsigned __int16 v35; // [rsp+4Ah] [rbp-4Eh] BYREF
  int v36; // [rsp+4Ch] [rbp-4Ch] BYREF
  _QWORD v37[9]; // [rsp+50h] [rbp-48h] BYREF

  if ( a7 != 0 )
  {
    v12 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 176, 1);
    if ( *(_DWORD *)(v12 + 16) != 0 )
      return 0;
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 171, 1);
    if ( *(_DWORD *)(v13 + 16) != 0 )
      return 0;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 168, 2);
    if ( *(__int16 *)(a1 + 168) <= 0 )
      *(_WORD *)(a1 + 168) = 1;
    v14 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 80, 4);
    if ( *(_DWORD *)(v14 + 16) != 0 )
      return 0;
    v15 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 96, 4);
    if ( *(_DWORD *)(v15 + 16) != 0 )
      return 0;
    v16 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 88, 4);
    if ( *(_DWORD *)(v16 + 16) != 0 )
      return 0;
    v17 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 120, 4);
    if ( *(_DWORD *)(v17 + 16) != 0 )
      return 0;
    v18 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 128, 4);
    if ( *(_DWORD *)(v18 + 16) != 0 )
      return 0;
    v19 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 152, 4);
    if ( *(_DWORD *)(v19 + 16) != 0 )
      return 0;
    v20 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 175, 1);
    if ( *(_DWORD *)(v20 + 16) != 0 )
      return 0;
    v21 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 104, 4);
    if ( *(_DWORD *)(v21 + 16) != 0 )
      return 0;
    v22 = *a2;
    (*(void (__fastcall **)(_QWORD, unsigned __int16 *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v35, 2);
    if ( *(_DWORD *)(v22 + 16) != 0 )
      return 0;
    if ( v35 != 0 )
    {
      sub_140893BE0(a1 + 56, v35);
      if ( v35 != 0 )
      {
        for ( i = 0; i < v35; sub_14083D020(a1 + 56, v37, i++) )
        {
          v24 = *a2;
          (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v36, 4);
          if ( *(_DWORD *)(v24 + 16) != 0 )
            return 0;
          v37[0] = v36;
        }
      }
    }
    v25 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 136, 4);
    if ( *(_DWORD *)(v25 + 16) != 0 )
      return 0;
    v26 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 144, 4);
    if ( *(_DWORD *)(v26 + 16) != 0 )
      return 0;
    v27 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 170, 1);
    if ( *(_DWORD *)(v27 + 16) != 0 )
      return 0;
    v28 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 172, 1);
    if ( *(_DWORD *)(v28 + 16) != 0 )
      return 0;
    v29 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 173, 1);
    if ( *(_DWORD *)(v29 + 16) != 0 )
      return 0;
    v30 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 174, 1);
    if ( *(_DWORD *)(v30 + 16) != 0 )
      return 0;
    v31 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 177, 1);
    if ( *(_DWORD *)(v31 + 16) != 0 )
      return 0;
    v32 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 112, 4);
    if ( *(_DWORD *)(v32 + 16) != 0 )
      return 0;
    v33 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 178, 1);
    if ( *(_DWORD *)(v33 + 16) != 0 )
      return 0;
  }
  if ( (_BYTE)a3 == 0 || (a3 = 0, (unsigned __int8)sub_1411C2780(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8) != 0) )
    LOBYTE(a3) = 1;
  return a3;
}
