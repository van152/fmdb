__int64 __fastcall sub_144354210(
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
  volatile signed __int32 *v16; // rbx
  volatile signed __int32 *v17; // rbx
  volatile signed __int32 *v18; // rbx
  volatile signed __int32 *v19; // rdi
  unsigned int *v20; // rbx
  __int64 v21; // r8

  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_12;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_14;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 80, 2);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_14;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 82, 2);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_14;
  v13 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 4);
  if ( *((_DWORD *)v13 + 4) != 0 )
    goto LABEL_14;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 84, 1);
  if ( *((_DWORD *)v14 + 4) != 0 )
    goto LABEL_14;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 85, 1);
  if ( *((_DWORD *)v15 + 4) != 0
    || (v16 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 86, 1),
        *((_DWORD *)v16 + 4) != 0)
    || (v17 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 76, 4),
        *((_DWORD *)v17 + 4) != 0)
    || (v18 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 87, 1),
        *((_DWORD *)v18 + 4) != 0)
    || (unsigned __int8)sub_140FEA0C0(v9 + 48, a2) == 0 )
  {
LABEL_14:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_12:
    v19 = *a2;
    if ( v19 != nullptr )
    {
      _InterlockedIncrement(v19 + 2);
      v20 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v19 + 40LL))(v19, v9 + 8, 12);
    }
    else
    {
      v20 = (unsigned int *)(v9 + 8);
    }
    v21 = *v20;
    if ( (unsigned int)v21 >= 0x989681 )
    {
      v21 = a6;
      *v20 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v21, a4);
    }
    LOBYTE(v9) = 1;
    if ( v19 != nullptr && _InterlockedDecrement(v19 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v19)(v19, 1);
  }
  return (unsigned int)v9;
}
