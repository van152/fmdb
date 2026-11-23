__int64 __fastcall sub_143FB7900(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        int a4,
        int a5,
        int a6,
        int a7,
        __int64 a8)
{
  volatile signed __int32 *v11; // rsi
  volatile signed __int32 *v12; // rsi
  int v13; // ebp
  volatile signed __int32 *v14; // rsi
  volatile signed __int32 *v15; // rsi
  volatile signed __int32 *v16; // rsi
  volatile signed __int32 *v17; // rsi
  volatile signed __int32 *v18; // rsi

  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v11 + 40LL))(v11, a1 + 24, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    return 0;
  v12 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v12 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(v12, a1 + 36, 4);
  }
  v13 = *((_DWORD *)v12 + 4);
  if ( _InterlockedDecrement(v12 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v12)(v12, 1);
  if ( v13 != 0 )
    return 0;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 52, 1);
  if ( *((_DWORD *)v14 + 4) != 0 )
    return 0;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 53, 1);
  if ( *((_DWORD *)v15 + 4) != 0 )
    return 0;
  v16 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 40, 4);
  if ( *((_DWORD *)v16 + 4) != 0 )
    return 0;
  v17 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 44, 4);
  if ( *((_DWORD *)v17 + 4) != 0 )
    return 0;
  v18 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 48, 4);
  if ( *((_DWORD *)v18 + 4) != 0 || (unsigned __int8)sub_140DB8980(a1 + 32, a2) == 0 )
    return 0;
  else
    return sub_140FAED40(a1, (_DWORD)a2, 0, a4, a5, a6, a7, a8);
}
