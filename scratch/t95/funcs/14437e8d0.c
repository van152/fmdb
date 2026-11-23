__int64 __fastcall sub_14437E8D0(
        __int64 a1,
        volatile signed __int32 **a2,
        __int64 a3,
        __int64 a4,
        int a5,
        unsigned int a6,
        char a7,
        __int64 a8)
{
  __int64 v9; // rsi
  volatile signed __int32 *v10; // rbx
  volatile signed __int32 *v11; // rbx
  volatile signed __int32 *v12; // rbx
  volatile signed __int32 *v13; // rbx
  volatile signed __int32 *v14; // rbx
  volatile signed __int32 *v15; // rbx
  volatile signed __int32 *v16; // rdi
  unsigned int *v17; // rbx
  __int64 v18; // r8

  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_10;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_12;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_12;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 52, 4);
  if ( *((_DWORD *)v12 + 4) != 0
    || (v13 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 60, 1),
        *((_DWORD *)v13 + 4) != 0)
    || (v14 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 56, 2),
        *((_DWORD *)v14 + 4) != 0)
    || (v15 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 58, 1),
        *((_DWORD *)v15 + 4) != 0)
    || (unsigned __int8)sub_140DB8980(v9 + 40, a2) == 0
    || (unsigned __int8)sub_140DB8980(v9 + 44, a2) == 0 )
  {
LABEL_12:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_10:
    v16 = *a2;
    if ( v16 != nullptr )
    {
      _InterlockedIncrement(v16 + 2);
      v17 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v16 + 40LL))(v16, v9 + 8, 12);
    }
    else
    {
      v17 = (unsigned int *)(v9 + 8);
    }
    v18 = *v17;
    if ( (unsigned int)v18 >= 0x989681 )
    {
      v18 = a6;
      *v17 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v18, a4);
    }
    LOBYTE(v9) = 1;
    if ( v16 != nullptr && _InterlockedDecrement(v16 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v16)(v16, 1);
  }
  return (unsigned int)v9;
}
