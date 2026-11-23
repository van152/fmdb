__int64 __fastcall sub_143FCDD90(
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
  __int64 v15; // r9
  volatile signed __int32 *v17; // rdi
  unsigned int *v18; // rbx
  __int64 v19; // r8

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
    goto LABEL_14;
  v12 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v12 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v12 + 40LL))(v12, v9 + 8, 4);
  }
  v13 = *((_DWORD *)v12 + 4);
  if ( _InterlockedDecrement(v12 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v12)(v12, 1);
  if ( v13 != 0
    || (v14 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 9, 1),
        *((_DWORD *)v14 + 4) != 0) )
  {
LABEL_14:
    LODWORD(v9) = 0;
  }
  else
  {
    v17 = *a2;
    if ( v17 != nullptr )
    {
      _InterlockedIncrement(v17 + 2);
      v18 = v9 + 2;
      (*(void (__fastcall **)(volatile signed __int32 *, _DWORD *, __int64))(*(_QWORD *)v17 + 40LL))(v17, v9 + 2, 12);
    }
    else
    {
      v18 = v9 + 2;
    }
    v19 = *v18;
    if ( (unsigned int)v19 >= 0x989681 )
    {
      v19 = a6;
      *v18 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v15) = 1;
      (*(void (__fastcall **)(__int64, _DWORD *, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v19, v15);
    }
    LOBYTE(v9) = 1;
    if ( v17 != nullptr && _InterlockedDecrement(v17 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v17)(v17, 1);
  }
  return (unsigned int)v9;
}
