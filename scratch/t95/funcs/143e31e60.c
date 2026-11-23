char __fastcall sub_143E31E60(__int64 a1, __int64 *a2)
{
  __int64 v3; // rax
  __int64 v4; // rcx
  _QWORD **v5; // r13
  _QWORD **v6; // r12
  _QWORD *v7; // r15
  __int64 v8; // rax
  char v9; // bl
  __int64 *v10; // rsi
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 v13; // rcx
  __int64 v15[3]; // [rsp+20h] [rbp-60h] BYREF
  int v16; // [rsp+38h] [rbp-48h] BYREF
  __int64 v17; // [rsp+40h] [rbp-40h] BYREF
  _QWORD v18[3]; // [rsp+50h] [rbp-30h] BYREF
  __int64 *v19; // [rsp+68h] [rbp-18h]
  _QWORD **v20; // [rsp+70h] [rbp-10h] BYREF
  _QWORD **v21; // [rsp+78h] [rbp-8h]
  __int64 v22; // [rsp+88h] [rbp+8h] BYREF
  _QWORD v23[10]; // [rsp+90h] [rbp+10h] BYREF

  v23[2] = -2;
  v19 = a2;
  sub_1407C9510(v18);
  do
  {
    sub_1407C9510(v15);
    (*(void (__fastcall **)(__int64, int *))(*(_QWORD *)a1 + 144LL))(a1, &v16);
    sub_140FEAD00(&v16, &v22);
    sub_140833EB0(v15, 1768169504, &v22);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
    sub_1407C9510(&v20);
    v3 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1751737714);
    if ( v3 == 0 )
      goto LABEL_8;
    (*(void (__fastcall **)(__int64, _QWORD ***))(*(_QWORD *)v3 + 256LL))(v3, &v20);
    v5 = v20;
    v6 = v21;
    if ( v20 == v21 )
      goto LABEL_8;
    while ( 1 )
    {
      v7 = *v5;
      v8 = sub_14083D4F0(v4);
      v23[1] = 0;
      v23[0] = v8 + 8;
      sub_140FEB270(&v22, v7);
      v9 = sub_140FEB670(&v16, &v22);
      (*(void (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)v23[0] + 16LL))(v23[0], v23);
      if ( v9 != 0 )
        break;
      if ( ++v5 == v6 )
      {
        v5 = v6;
        break;
      }
    }
    if ( v5 == v21 )
    {
LABEL_8:
      sub_140FEAD00(&v16, &v22);
      sub_14083B5F0(&v20, &v22);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
    }
    if ( v21 != v20 )
    {
      sub_14083DB80(&v22, &v20);
      sub_140833EB0(v15, 1936286323, &v22);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
    }
    sub_14083DDA0(&v22, v15);
    sub_14083BBE0(v18, &v22, 0);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
    a1 = (*(__int64 (__fastcall **)(__int64, __int64))(*(_QWORD *)a1 + 80LL))(a1, 1751737714);
    sub_14083B0A0(&v20);
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, &v17);
    sub_140833970(v15);
  }
  while ( a1 != 0 );
  sub_14083DB80(&v22, v18);
  v10 = v19;
  v11 = *v19;
  if ( &v22 != v19 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v11 + 16LL))(v11, v19);
    v12 = v22;
    v13 = v23[0];
    v10[1] = v23[0];
    *v10 = v12;
    v11 = sub_14083D4F0(v13) + 8;
    v23[0] = 0;
    v22 = v11;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v11 + 16LL))(v11, &v22);
  sub_14083B0A0(v18);
  return 1;
}
