__int64 __fastcall sub_1444C31F0(
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
  volatile signed __int32 *v15; // rdi
  unsigned int *v16; // rbx
  __int64 v17; // r8

  v9 = a1;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0
    || (v11 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 28, 4),
        *((_DWORD *)v11 + 4) != 0)
    || (v12 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 2),
        *((_DWORD *)v12 + 4) != 0) )
  {
    LODWORD(v9) = 0;
  }
  else
  {
    v15 = *a2;
    if ( v15 != nullptr )
    {
      _InterlockedIncrement(v15 + 2);
      v16 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v15 + 40LL))(v15, v9 + 8, 12);
    }
    else
    {
      v16 = (unsigned int *)(v9 + 8);
    }
    v17 = *v16;
    if ( (unsigned int)v17 >= 0x989681 )
    {
      v17 = a6;
      *v16 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v13) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v17, v13);
    }
    LOBYTE(v9) = 1;
    if ( v15 != nullptr && _InterlockedDecrement(v15 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v15)(v15, 1);
  }
  return (unsigned int)v9;
}
