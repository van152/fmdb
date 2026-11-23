__int64 __fastcall sub_1444C4820(
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
  __int64 v11; // r9
  volatile signed __int32 *v12; // rdi
  unsigned int *v13; // rbx
  __int64 v15; // r8

  v9 = a1;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 40, 4);
  if ( *((_DWORD *)v10 + 4) != 0 || (unsigned __int8)sub_141731DA0(v9 + 24, a2) == 0 )
  {
    LODWORD(v9) = 0;
  }
  else
  {
    v12 = *a2;
    if ( v12 != nullptr )
    {
      _InterlockedIncrement(v12 + 2);
      v13 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(v12, v9 + 8, 12);
    }
    else
    {
      v13 = (unsigned int *)(v9 + 8);
    }
    v15 = *v13;
    if ( (unsigned int)v15 >= 0x989681 )
    {
      v15 = a6;
      *v13 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(v11) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v15, v11);
    }
    LOBYTE(v9) = 1;
    if ( v12 != nullptr && _InterlockedDecrement(v12 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v12)(v12, 1);
  }
  return (unsigned int)v9;
}
