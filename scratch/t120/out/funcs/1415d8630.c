__int64 __fastcall sub_1415D8630(
        __int64 a1,
        _QWORD *a2,
        unsigned int a3,
        __int64 a4,
        int a5,
        int a6,
        char a7,
        __int64 a8)
{
  __int64 v11; // rbx
  __int64 v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  bool v17; // al
  int v19; // [rsp+30h] [rbp-68h]
  _BYTE v20[8]; // [rsp+48h] [rbp-50h] BYREF
  int v21[18]; // [rsp+50h] [rbp-48h] BYREF

  v11 = a1 + -*(_DWORD *)(a1 - 4);
  if ( a7 != 0 )
  {
    sub_140F9F4A0(a1: v20);
    if ( *(unsigned __int16 *)(a4 + 1416) <= 0xDC9u )
    {
      v21[0] = -1;
      v12 = *a2;
      (*(void (__fastcall **)(_QWORD, int *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v21, a3: 4);
      if ( *(_DWORD *)(v12 + 16) != 0 )
        goto LABEL_9;
    }
    v13 = *a2;
    (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 16, a3: 1);
    if ( *(_DWORD *)(v13 + 16) != 0
      || (v14 = *a2,
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 14, a3: 1),
          *(_DWORD *)(v14 + 16) != 0)
      || (v15 = *a2,
          (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 13, a3: 1),
          *(_DWORD *)(v15 + 16) != 0)
      || (unsigned __int8)sub_140F81270(a1: v11 - 24, a2, a3: 1) == 0 )
    {
LABEL_9:
      v17 = false;
    }
    else
    {
      v16 = *a2;
      (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: v11 - 15, a3: 1);
      v17 = *(_DWORD *)(v16 + 16) == 0;
    }
    if ( v20[0] != 0 )
    {
      if ( v17 )
        goto LABEL_12;
    }
    else
    {
      byte_141B5FC2C = 0;
      if ( v17 )
        goto LABEL_12;
    }
    return 0;
  }
LABEL_12:
  if ( (_BYTE)a3 == 0
    || (a3 = 0, (unsigned __int8)sub_140DFB5C0(a1: (int)v11 - 16, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8) != 0)
    && (LOBYTE(v19) = a7,
        a3 = 0,
        (unsigned __int8)sub_141084540(a1: v11, (_DWORD)a2, a3: 0, a4, a5, a6, a7: v19, a8) != 0) )
  {
    LOBYTE(a3) = 1;
  }
  return a3;
}
