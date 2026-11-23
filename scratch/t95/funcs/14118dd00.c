__int64 __fastcall sub_14118DD00(
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
  volatile signed __int32 *v28; // rbx
  volatile signed __int32 *v29; // rbx
  volatile signed __int32 *v30; // rbx
  volatile signed __int32 *v31; // rbx
  volatile signed __int32 *v32; // rdi
  unsigned int *v33; // rbx
  __int64 v34; // r8
  int v36; // [rsp+28h] [rbp-30h] BYREF
  int v37; // [rsp+30h] [rbp-28h] BYREF
  int v38[8]; // [rsp+38h] [rbp-20h] BYREF

  v9 = a1;
  if ( a7 == 0 )
    goto LABEL_31;
  v10 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, a1 + 24, 4);
  if ( *((_DWORD *)v10 + 4) != 0 )
    goto LABEL_30;
  v11 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 140, 2);
  if ( *((_DWORD *)v11 + 4) != 0 )
    goto LABEL_30;
  v12 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 32, 4);
  if ( *((_DWORD *)v12 + 4) != 0 )
    goto LABEL_30;
  v13 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 48, 4);
  if ( *((_DWORD *)v13 + 4) != 0 )
    goto LABEL_30;
  v14 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 72, 4);
  if ( *((_DWORD *)v14 + 4) != 0 )
    goto LABEL_30;
  v15 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 142, 2);
  if ( *((_DWORD *)v15 + 4) != 0 )
    goto LABEL_30;
  v16 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 146, 2);
  if ( *((_DWORD *)v16 + 4) != 0 )
    goto LABEL_30;
  v17 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 150, 2);
  if ( *((_DWORD *)v17 + 4) != 0 )
    goto LABEL_30;
  v18 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 144, 2);
  if ( *((_DWORD *)v18 + 4) != 0 )
    goto LABEL_30;
  v19 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 148, 2);
  if ( *((_DWORD *)v19 + 4) != 0 )
    goto LABEL_30;
  v20 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 152, 2);
  if ( *((_DWORD *)v20 + 4) != 0 )
    goto LABEL_30;
  v21 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 128, 4);
  if ( *((_DWORD *)v21 + 4) != 0 )
    goto LABEL_30;
  v22 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 132, 4);
  if ( *((_DWORD *)v22 + 4) != 0 )
    goto LABEL_30;
  v23 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 136, 4);
  if ( *((_DWORD *)v23 + 4) != 0 )
    goto LABEL_30;
  sub_140814B10(*a2, v38, v9 + 80);
  if ( v38[0] != 0 )
    goto LABEL_30;
  sub_140814B10(*a2, &v37, v9 + 88);
  if ( v37 != 0 )
    goto LABEL_30;
  sub_140814B10(*a2, &v36, v9 + 96);
  if ( v36 != 0 )
    goto LABEL_30;
  if ( (unsigned __int8)sub_140FEA0C0(v9 + 104, a2) == 0 )
    goto LABEL_30;
  if ( (unsigned __int8)sub_140FEA0C0(v9 + 112, a2) == 0 )
    goto LABEL_30;
  if ( (unsigned __int8)sub_140FEA0C0(v9 + 120, a2) == 0 )
    goto LABEL_30;
  v24 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 40, 4);
  if ( *((_DWORD *)v24 + 4) != 0 )
    goto LABEL_30;
  v25 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 56, 4);
  if ( *((_DWORD *)v25 + 4) != 0 )
    goto LABEL_30;
  v26 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 64, 4);
  if ( *((_DWORD *)v26 + 4) != 0 )
    goto LABEL_30;
  v27 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 155, 1);
  if ( *((_DWORD *)v27 + 4) != 0 )
    goto LABEL_30;
  v28 = *a2;
  (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 156, 1);
  if ( *((_DWORD *)v28 + 4) != 0
    || (v29 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 154, 1),
        *((_DWORD *)v29 + 4) != 0)
    || (v30 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 157, 1),
        *((_DWORD *)v30 + 4) != 0)
    || (v31 = *a2,
        (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v9 + 158, 1),
        *((_DWORD *)v31 + 4) != 0) )
  {
LABEL_30:
    LODWORD(v9) = 0;
  }
  else
  {
LABEL_31:
    v32 = *a2;
    if ( v32 != nullptr )
    {
      _InterlockedIncrement(v32 + 2);
      v33 = (unsigned int *)(v9 + 8);
      (*(void (__fastcall **)(volatile signed __int32 *, __int64, __int64))(*(_QWORD *)v32 + 40LL))(v32, v9 + 8, 12);
    }
    else
    {
      v33 = (unsigned int *)(v9 + 8);
    }
    v34 = *v33;
    if ( (unsigned int)v34 >= 0x989681 )
    {
      v34 = a6;
      *v33 = a6;
    }
    if ( a8 != 0 )
    {
      LOBYTE(a4) = 1;
      (*(void (__fastcall **)(__int64, __int64, __int64, __int64))(*(_QWORD *)a8 + 24LL))(a8, v9, v34, a4);
    }
    LOBYTE(v9) = 1;
    if ( v32 != nullptr && _InterlockedDecrement(v32 + 2) == 0 )
      (**(void (__fastcall ***)(volatile signed __int32 *, __int64))v32)(v32, 1);
  }
  return (unsigned int)v9;
}
