bool __fastcall sub_144381B80(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        int a7,
        __int64 a8)
{
  volatile signed __int32 *v10; // rdi
  int v11; // ebp
  volatile signed __int32 *v13; // rdi
  volatile signed __int32 *v14; // r14
  unsigned int *v15; // rbx
  char v16; // r15
  __int64 v17; // r8

  v10 = *a2;
  if ( *a2 != nullptr )
  {
    _InterlockedIncrement(v10 + 2);
    (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v10 + 40LL))(v10, a1 + 36, 4);
  }
  v11 = *((_DWORD *)v10 + 4);
  if ( _InterlockedDecrement(v10 + 2) == 0 )
    (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v10)(v10, 1);
  if ( v11 == 0 )
  {
    v13 = *a2;
    if ( *a2 != nullptr
      && (_InterlockedIncrement(v13 + 2),
          (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(
            v13,
            a1 + 24,
            12),
          (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v13 + 40LL))(v13, a1 + 40, 7),
          v14 = *a2,
          *a2 != nullptr) )
    {
      _InterlockedIncrement(v14 + 2);
      v15 = (unsigned int *)(a1 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v14 + 40LL))(v14, a1 + 8, 12);
      v16 = 0;
    }
    else
    {
      v15 = (unsigned int *)(a1 + 8);
      v16 = 1;
      v14 = nullptr;
    }
    v17 = *v15;
    if ( (unsigned int)v17 >= 0x989681 )
    {
      v17 = a6;
      *v15 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, a1, v17, a4);
    }
    if ( v16 == 0 && _InterlockedDecrement(v14 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v14)(v14, 1);
    if ( v13 != nullptr && _InterlockedDecrement(v13 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v13)(v13, 1);
  }
  return v11 == 0;
}
