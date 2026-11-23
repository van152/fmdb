__int64 __fastcall sub_144556790(
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
  __int64 v12; // r9
  volatile signed __int32 *v14; // rdi
  unsigned int *v15; // rbx
  __int64 v16; // r8

  v9 = a1;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 32, 1);
  if ( *((_DWORD *)v10 + 4) != 0
    || (v11 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 33, 1),
        *((_DWORD *)v11 + 4) != 0) )
  {
    LODWORD(v9) = 0;
  }
  else
  {
    v14 = *a2;
    if ( v14 != nullptr )
    {
      _InterlockedIncrement(v14 + 2);
      v15 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v14 + 40LL))(v14, v9 + 8, 12);
    }
    else
    {
      v15 = (unsigned int *)(v9 + 8);
    }
    v16 = *v15;
    if ( (unsigned int)v16 >= 0x989681 )
    {
      v16 = a6;
      *v15 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v12) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v16, v12);
    }
    LOBYTE(v9) = 1;
    if ( v14 != nullptr && _InterlockedDecrement(v14 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v14)(v14, 1);
  }
  return (unsigned int)v9;
}
