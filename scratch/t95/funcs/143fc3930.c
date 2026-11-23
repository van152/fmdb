__int64 __fastcall sub_143FC3930(__int64 a1, _QWORD *a2, __int64 a3, int a4, int a5, int a6, int a7, __int64 a8)
{
  _DWORD *v11; // rsi
  _DWORD *v12; // rsi
  __int64 v13; // rsi
  int v14; // ebp
  __int64 v15; // rsi
  int v16; // ebp
  __int64 v17; // rsi
  __int64 v18; // rsi
  __int64 v19; // rsi
  __int64 v20; // rsi
  __int64 v21; // rsi

  v11 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_DWORD *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 24, 4);
  if ( v11[4] != 0 )
    return 0;
  v12 = (_DWORD *)*a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 32, 4);
  if ( v12[4] != 0 )
    return 0;
  v13 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v13 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v13 + 40LL))(v13, a1 + 40, 4);
  }
  v14 = *(_DWORD *)(v13 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v13 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v13)(v13, 1);
  if ( v14 != 0 )
    return 0;
  v15 = *a2;
  if ( *a2 != 0 )
  {
    _InterlockedIncrement((volatile signed __int32 *)(v15 + 8));
    (*(void (__fastcall **)(__int64, __int64, __int64))(*(_QWORD *)v15 + 40LL))(v15, a1 + 44, 4);
  }
  v16 = *(_DWORD *)(v15 + 16);
  if ( _InterlockedDecrement((volatile signed __int32 *)(v15 + 8)) == 0 )
    (**(void (__fastcall ***)(__int64, __int64))v15)(v15, 1);
  if ( v16 != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 1);
  if ( *(_DWORD *)(v17 + 16) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 49, 1);
  if ( *(_DWORD *)(v18 + 16) != 0 )
    return 0;
  v19 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 50, 1);
  if ( *(_DWORD *)(v19 + 16) != 0 )
    return 0;
  v20 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 51, 1);
  if ( *(_DWORD *)(v20 + 16) != 0 )
    return 0;
  v21 = *a2;
  (*(void (__fastcall **)(_QWORD, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 1);
  if ( *(_DWORD *)(v21 + 16) != 0 )
    return 0;
  else
    return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
