__int64 __fastcall sub_1444DD8A0(
        _DWORD *a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  _DWORD *v9; // rsi
  volatile signed __int32 *v10; // rbx
  int v11; // ebp
  volatile signed __int32 *v12; // rbx
  int v13; // ebp
  volatile signed __int32 *v14; // rbx
  int v15; // ebp
  volatile signed __int32 *v16; // rbx
  int v17; // ebp
  volatile signed __int32 *v18; // rbx
  __int64 v19; // r9
  volatile signed __int32 *v21; // rdi
  unsigned int *v22; // rbx
  __int64 v23; // r8

  v9 = a1;
  v10 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v10 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 6, 8);
  }
  if ( v9[7] == 0 )
    v9[7] = v9[6];
  v11 = *((_DWORD *)v10 + 4);
  if ( _InterlockedDecrement(v10 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v10)(v10, 1);
  if ( v11 != 0 )
    goto LABEL_28;
  v12 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v12 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v9 + 8, 8);
  }
  if ( v9[9] == 0 )
    v9[9] = v9[8];
  v13 = *((_DWORD *)v12 + 4);
  if ( _InterlockedDecrement(v12 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v12)(v12, 1);
  if ( v13 != 0 )
    goto LABEL_28;
  v14 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v14 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v14 + 40LL))(v14, v9 + 10, 8);
  }
  if ( v9[11] == 0 )
    v9[11] = v9[10];
  v15 = *((_DWORD *)v14 + 4);
  if ( _InterlockedDecrement(v14 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v14)(v14, 1);
  if ( v15 != 0 )
    goto LABEL_28;
  v16 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v16 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v16 + 40LL))(v16, v9 + 12, 4);
  }
  v17 = *((_DWORD *)v16 + 4);
  if ( _InterlockedDecrement(v16 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v16)(v16, 1);
  if ( v17 != 0
    || (v18 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 13, 4),
        *((_DWORD *)v18 + 4) != 0) )
  {
LABEL_28:
    LODWORD(v9) = 0;
  }
  else
  {
    v21 = *a2;
    if ( v21 != nullptr )
    {
      _InterlockedIncrement(v21 + 2);
      v22 = v9 + 2;
      (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v21 + 40LL))(v21, v9 + 2, 12);
    }
    else
    {
      v22 = v9 + 2;
    }
    v23 = *v22;
    if ( (unsigned int)v23 >= 0x989681 )
    {
      v23 = a6;
      *v22 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v19) = 1;
      (*(void (__fastcall **)(__int64, _DWORD *, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v23, v19);
    }
    LOBYTE(v9) = 1;
    if ( v21 != nullptr && _InterlockedDecrement(v21 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v21)(v21, 1);
  }
  return (unsigned int)v9;
}
