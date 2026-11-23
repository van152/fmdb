__int64 __fastcall sub_143FFF990(_BYTE *a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  __int64 v11; // rsi
  __int64 v12; // rsi
  __int64 v13; // rsi
  __int64 v14; // rsi
  __int64 v15; // rsi
  __int64 v16; // rsi
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  char v21; // [rsp+46h] [rbp-32h] BYREF
  char v22; // [rsp+47h] [rbp-31h] BYREF
  int v23; // [rsp+48h] [rbp-30h] BYREF
  _DWORD v24[10]; // [rsp+50h] [rbp-28h] BYREF

  v11 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v21, a3: 1);
  if ( *(_DWORD *)(v11 + 16) != 0 )
    return 0;
  a1[40] = v21;
  v12 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v21, a3: 1);
  if ( *(_DWORD *)(v12 + 16) != 0 )
    return 0;
  a1[47] = v21;
  v13 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 41, a3: 1);
  if ( *(_DWORD *)(v13 + 16) != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v22, a3: 1);
  if ( *(_DWORD *)(v14 + 16) != 0 )
    return 0;
  a1[44] = v22;
  v15 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 45, a3: 1);
  if ( *(_DWORD *)(v15 + 16) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 46, a3: 1);
  if ( *(_DWORD *)(v16 + 16) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 48, a3: 4);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  sub_140814B10(a1: *a2, a2: v24, a3: a1 + 24);
  if ( v24[0] != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 42, a3: 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  sub_140814B10(a1: *a2, a2: &v23, a3: a1 + 32);
  if ( v23 != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, _BYTE *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a1 + 43, a3: 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  else
    return sub_140FAED40((_DWORD)a1, (_DWORD)a2, a3: 0, a4, a5, a6, a7, a8);
}
