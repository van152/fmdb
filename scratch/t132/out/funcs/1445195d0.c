__int64 __fastcall sub_1445195D0(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  unsigned int v10; // ebx
  __int64 v11; // r9
  volatile signed __int32 *v12; // rdi
  unsigned int *v13; // r15
  __int64 v14; // r8

  v10 = sub_1415782C0();
  if ( (_BYTE)v10 != 0 && a8 != 0 )
  {
    v12 = *a2;
    if ( v12 != nullptr )
    {
      _InterlockedIncrement(v12 + 2);
      v13 = (unsigned int *)(a1 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v12 + 40LL))(
        a1: v12,
        a2: a1 + 8,
        a3: 12);
    }
    else
    {
      v13 = (unsigned int *)(a1 + 8);
    }
    v14 = *v13;
    if ( (unsigned int)v14 >= 0x989681 )
    {
      v14 = a6;
      *v13 = a6;
    }
    LOBYTE(v11) = 1;
    (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(
      a1: a8,
      a2: a1,
      a3: v14,
      a4: v11);
    if ( v12 != nullptr && _InterlockedDecrement(v12 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v12)(a1: v12, a2: 1);
  }
  return v10;
}
