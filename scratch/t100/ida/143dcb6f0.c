char __fastcall sub_143DCB6F0(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  volatile signed __int32 *v9; // rsi
  unsigned int *v10; // rbx
  __int64 v11; // r8

  v9 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v9 + 2);
    v10 = (unsigned int *)(a1 + 8);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v9 + 40LL))(v9, a1 + 8, 12);
  }
  else
  {
    v10 = (unsigned int *)(a1 + 8);
  }
  v11 = *v10;
  if ( (unsigned int)v11 >= 0x989681 )
  {
    v11 = a6;
    *v10 = a6;
  }
  if ( a8 != 0 )
  {
    LOBYTE(a4) = 1;
    (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v11, a4);
  }
  if ( v9 != nullptr && _InterlockedDecrement(v9 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v9)(v9, 1);
  return 1;
}
