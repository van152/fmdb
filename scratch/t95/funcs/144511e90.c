__int64 __fastcall sub_144511E90(
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
  volatile signed __int32 *v19; // rbx
  volatile signed __int32 *v20; // rbx
  volatile signed __int32 *v21; // rdi
  unsigned int *v22; // rbx
  __int64 v23; // r8

  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_14;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_13;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_13;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 72, 2);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_13;
  v13 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 74, 2);
  if ( *((_DWORD *)v13 + 4) != 0 )
    goto LABEL_13;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 48, 4);
  if ( *((_DWORD *)v14 + 4) != 0 )
    goto LABEL_13;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 56, 4);
  if ( *((_DWORD *)v15 + 4) != 0 )
    goto LABEL_13;
  v16 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 76, 1);
  if ( *((_DWORD *)v16 + 4) != 0 )
    goto LABEL_13;
  v17 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 77, 1);
  if ( *((_DWORD *)v17 + 4) != 0
    || (v18 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 40, 4),
        *((_DWORD *)v18 + 4) != 0)
    || (v19 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 78, 1),
        *((_DWORD *)v19 + 4) != 0)
    || (v20 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 64, 4),
        *((_DWORD *)v20 + 4) != 0) )
  {
LABEL_13:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_14:
    v21 = *a2;
    if ( v21 != nullptr )
    {
      _InterlockedIncrement(v21 + 2);
      v22 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v21 + 40LL))(v21, v9 + 8, 12);
    }
    else
    {
      v22 = (unsigned int *)(v9 + 8);
    }
    v23 = *v22;
    if ( (unsigned int)v23 >= 0x989681 )
    {
      v23 = a6;
      *v22 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v23, a4);
    }
    LOBYTE(v9) = 1;
    if ( v21 != nullptr && _InterlockedDecrement(v21 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v21)(v21, 1);
  }
  return (unsigned int)v9;
}
