__int64 __fastcall sub_141544130(_DWORD *a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, char a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  int v14; // ebp
  __int64 v15; // rsi
  int v16; // ebp
  __int64 v17; // rsi
  int v18; // ebp
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi
  __int64 v22; // rsi
  __int64 v23; // rsi
  __int64 v24; // rsi
  __int64 v25; // rsi
  __int64 v26; // rsi
  _DWORD v28[12]; // [rsp+48h] [rbp-30h] BYREF

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, _DWORD *, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 19, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 94, 1);
  if ( v12[4] != 0 )
    return 0;
  v13 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
    (*(void (__fastcall **)(__int64, _DWORD *, __int64))(*(_QWORD *)v13 + 40LL))(v13, a1 + 6, 8);
  }
  if ( a1[7] == 0 )
    a1[7] = a1[6];
  v14 = *(_DWORD *)(v13 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v13)(v13, 1);
  if ( v14 != 0 )
    return 0;
  v15 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v15 + 8));
    (*(void (__fastcall **)(__int64, _DWORD *, __int64))(*(_QWORD *)v15 + 40LL))(v15, a1 + 8, 8);
  }
  if ( a1[9] == 0 )
    a1[9] = a1[8];
  v16 = *(_DWORD *)(v15 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v15)(v15, 1);
  if ( v16 != 0 )
    return 0;
  v17 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v17 + 8));
    (*(void (__fastcall **)(__int64, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, a1 + 10, 8);
  }
  if ( a1[11] == 0 )
    a1[11] = a1[10];
  v18 = *(_DWORD *)(v17 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v17 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v17)(v17, 1);
  if ( v18 != 0 )
    return 0;
  if ( (unsigned __int8)sub_140FEA0C0(a1 + 12, a2) == 0 )
    return 0;
  sub_140814B10(*a2, v28, a1 + 14);
  if ( v28[0] != 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1 + 16, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1 + 17, a2) == 0 )
    return 0;
  if ( (unsigned __int8)sub_140DB8980(a1 + 18, a2) == 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 20, 4);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 21, 2);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 86, 2);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  v22 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 22, 2);
  if ( *(_DWORD *)(v22 + 16) != 0 )
    return 0;
  v23 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 90, 1);
  if ( *(_DWORD *)(v23 + 16) != 0 )
    return 0;
  v24 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 91, 1);
  if ( *(_DWORD *)(v24 + 16) != 0 )
    return 0;
  v25 = *a2;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 23, 1);
  if ( *(_DWORD *)(v25 + 16) != 0 )
    return 0;
  v26 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, (__int64)a1 + 93, 1);
  if ( *(_DWORD *)(v26 + 16) != 0 )
    return 0;
  else
    return sub_140FAED40((_DWORD)a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
