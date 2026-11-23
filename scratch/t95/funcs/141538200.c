__int64 __fastcall sub_141538200(
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
  volatile signed __int32 *v21; // rbx
  volatile signed __int32 *v22; // rbx
  volatile signed __int32 *v23; // rbx
  volatile signed __int32 *v24; // rbx
  volatile signed __int32 *v25; // rbx
  volatile signed __int32 *v26; // rbx
  volatile signed __int32 *v27; // rbx
  volatile signed __int32 *v29; // rdi
  unsigned int *v30; // rbx
  __int64 v31; // r8

  if ( a4 == 0 )
    goto LABEL_24;
  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_26;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_24;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 4);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_24;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 40, 4);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_24;
  if ( (unsigned __int8)sub_140DB8980(v9 + 48, a2) == 0 )
    goto LABEL_24;
  if ( (unsigned __int8)sub_140DB8980(v9 + 52, a2) == 0 )
    goto LABEL_24;
  v13 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 60, 4);
  if ( *((_DWORD *)v13 + 4) != 0 )
    goto LABEL_24;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 100, 1);
  if ( *((_DWORD *)v14 + 4) != 0 )
    goto LABEL_24;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 72, 4);
  if ( *((_DWORD *)v15 + 4) != 0 )
    goto LABEL_24;
  v16 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 101, 1);
  if ( *((_DWORD *)v16 + 4) != 0 )
    goto LABEL_24;
  v17 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 64, 4);
  if ( *((_DWORD *)v17 + 4) != 0 )
    goto LABEL_24;
  v18 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 80, 4);
  if ( *((_DWORD *)v18 + 4) != 0 )
    goto LABEL_24;
  v19 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 84, 4);
  if ( *((_DWORD *)v19 + 4) != 0 )
    goto LABEL_24;
  v20 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 88, 4);
  if ( *((_DWORD *)v20 + 4) != 0 )
    goto LABEL_24;
  v21 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 92, 4);
  if ( *((_DWORD *)v21 + 4) != 0 )
    goto LABEL_24;
  if ( (unsigned __int8)sub_140DB8980(v9 + 56, a2) == 0 )
    goto LABEL_24;
  v22 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 102, 1);
  if ( *((_DWORD *)v22 + 4) != 0 )
    goto LABEL_24;
  v23 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 96, 4);
  if ( *((_DWORD *)v23 + 4) != 0 )
    goto LABEL_24;
  v24 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 105, 1);
  if ( *((_DWORD *)v24 + 4) != 0
    || (v25 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 103, 1),
        *((_DWORD *)v25 + 4) != 0)
    || (v26 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 104, 1),
        *((_DWORD *)v26 + 4) != 0)
    || (v27 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 68, 4),
        *((_DWORD *)v27 + 4) != 0) )
  {
LABEL_24:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_26:
    v29 = *a2;
    if ( v29 != nullptr )
    {
      _InterlockedIncrement(v29 + 2);
      v30 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v29 + 40LL))(v29, v9 + 8, 12);
    }
    else
    {
      v30 = (unsigned int *)(v9 + 8);
    }
    v31 = *v30;
    if ( (unsigned int)v31 >= 0x989681 )
    {
      v31 = a6;
      *v30 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v31, a4);
    }
    LOBYTE(v9) = 1;
    if ( v29 != nullptr && _InterlockedDecrement(v29 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v29)(v29, 1);
  }
  return (unsigned int)v9;
}
