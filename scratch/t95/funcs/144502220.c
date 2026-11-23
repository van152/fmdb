__int64 __fastcall sub_144502220(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  __int64 v9; // rdi
  volatile signed __int32 *v10; // rsi
  unsigned int *v11; // rbx
  __int64 v12; // r8

  v9 = a1;
  if ( a7 != 0 && (unsigned __int8)sub_1409FA4B0(a1 + 24, a2) == 0 )
  {
    LODWORD(v9) = 0;
  }
  else
  {
    v10 = *a2;
    if ( v10 != nullptr )
    {
      _InterlockedIncrement(v10 + 2);
      v11 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, v9 + 8, 12);
    }
    else
    {
      v11 = (unsigned int *)(v9 + 8);
    }
    v12 = *v11;
    if ( (unsigned int)v12 >= 0x989681 )
    {
      v12 = a6;
      *v11 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v12, a4);
    }
    LOBYTE(v9) = 1;
    if ( v10 != nullptr && _InterlockedDecrement(v10 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v10)(v10, 1);
  }
  return (unsigned int)v9;
}
