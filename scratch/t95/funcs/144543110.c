__int64 __fastcall sub_144543110(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  __int64 v9; // rsi
  volatile signed __int32 *v10; // rbx
  volatile signed __int32 *v11; // rbx
  volatile signed __int32 *v12; // rbx
  __int64 v13; // r9
  volatile signed __int32 *v14; // rbx
  int v15; // ebp
  volatile signed __int32 *v17; // rdi
  unsigned int *v18; // rbx
  __int64 v19; // r8

  v9 = a1;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_9;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 28, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_9;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 36, 1);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_9;
  v14 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v14 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v14 + 40LL))(v14, v9 + 32, 4);
  }
  v15 = *((_DWORD *)v14 + 4);
  if ( _InterlockedDecrement(v14 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v14)(v14, 1);
  if ( v15 != 0 )
  {
LABEL_9:
    LODWORD(v9) = 0;
  }
  else
  {
    v17 = *a2;
    if ( v17 != nullptr )
    {
      _InterlockedIncrement(v17 + 2);
      v18 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v17 + 40LL))(v17, v9 + 8, 12);
    }
    else
    {
      v18 = (unsigned int *)(v9 + 8);
    }
    v19 = *v18;
    if ( (unsigned int)v19 >= 0x989681 )
    {
      v19 = a6;
      *v18 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v13) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v19, v13);
    }
    LOBYTE(v9) = 1;
    if ( v17 != nullptr && _InterlockedDecrement(v17 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v17)(v17, 1);
  }
  return (unsigned int)v9;
}
