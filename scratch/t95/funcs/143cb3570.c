__int64 __fastcall sub_143CB3570(__int64 a1, _QWORD *a2, __int64 a3, __int64 a4, int a5, int a6, int a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rdx
  int v19; // [rsp+20h] [rbp-38h] BYREF
  _QWORD v20[6]; // [rsp+28h] [rbp-30h] BYREF

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 240, 1);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 241, 1);
  if ( v12[4] != 0 )
    return 0;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 242, 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 228, 4);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 243, 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 244, 1);
  if ( *(_DWORD *)(v16 + 16) != 0 || (unsigned __int8)sub_14150F650(a1 + 72, a2) == 0 )
    return 0;
  if ( (_BYTE)a7 == 0 )
    return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
  *(_QWORD *)(a1 + 96) = 0;
  v20[0] = a2;
  if ( *(unsigned __int16 *)(a4 + 1416) < 0xDC5u )
  {
    v17 = a1 + 120;
    goto LABEL_16;
  }
  if ( (unsigned __int8)sub_140ED6950(v20, a1 + 104) == 0 || (unsigned __int8)sub_140ED6950(v20, a1 + 112) == 0 )
    return 0;
  if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC6u )
  {
    if ( (unsigned __int8)sub_140ED6950(v20, a1 + 120) == 0 )
      return 0;
    v17 = a1 + 128;
LABEL_16:
    if ( (unsigned __int8)sub_140ED6950(v20, v17) != 0 )
      goto LABEL_17;
    return 0;
  }
LABEL_17:
  if ( (unsigned __int8)sub_140ED6950(v20, a1 + 136) == 0 )
    return 0;
  if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC5u )
  {
    if ( (unsigned __int8)sub_140ED6950(v20, a1 + 144) == 0 )
      return 0;
    if ( *(unsigned __int16 *)(a4 + 1416) >= 0xDC6u )
    {
      sub_140839290(*a2, &v19, a1 + 152);
      if ( v19 != 0 )
        return 0;
      sub_140839290(*a2, &v19, a1 + 176);
      if ( v19 != 0 )
        return 0;
    }
  }
  return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
