__int64 __fastcall sub_1444ECE40(int *a1, __int64 *a2)
{
  __int64 v4; // rcx
  __int64 v5; // rax
  __int64 v6; // rdi
  __int64 v7; // rbx
  unsigned __int64 v8; // rsi
  __int64 v9; // rdi
  __int64 i; // r14
  __int64 *v11; // rdx
  int v12; // esi
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rcx
  int v16; // esi
  __int64 v17; // rax
  __int64 v18; // rax
  __int64 *v19; // rdi
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v24; // [rsp+28h] [rbp-58h] BYREF
  __int64 v25; // [rsp+30h] [rbp-50h]
  __int64 *v26; // [rsp+40h] [rbp-40h]
  __int64 v27; // [rsp+48h] [rbp-38h] BYREF
  __int64 v28; // [rsp+50h] [rbp-30h]
  __int64 v29; // [rsp+58h] [rbp-28h] BYREF
  int v30; // [rsp+60h] [rbp-20h]
  __int64 v31; // [rsp+68h] [rbp-18h]
  __int64 v32; // [rsp+70h] [rbp-10h] BYREF
  __int64 v33; // [rsp+78h] [rbp-8h]
  __int64 v34; // [rsp+80h] [rbp+0h]

  v34 = -2;
  sub_1407C9510(&v24);
  v5 = sub_14083D4F0(v4);
  v30 = 1299478896;
  v29 = v5 + 56;
  sub_14083B5F0(&v24, &v29);
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v29 + 16LL))(v29, &v29);
  v26 = a2;
  sub_1407C9510(&v29);
  v6 = v24;
  v7 = v25;
  v8 = (v25 - v24) >> 3;
  if ( (v31 - v29) >> 4 < v8 )
  {
    if ( (unsigned __int64)(v25 - v24) >= 0x7FFFFFFFFFFFFFF9LL )
      sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
    sub_140837DD0(&v29, (v25 - v24) >> 3);
  }
  if ( v7 != v6 )
  {
    v9 = 1;
    if ( v8 >= 2 )
      v9 = v8;
    for ( i = 0; i != v9; ++i )
    {
      v11 = *(__int64 **)(v24 + 8 * i);
      if ( v11 == nullptr )
        v11 = &qword_141B5A4A0;
      v12 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v11 + 80LL))(*v11);
      v14 = sub_14083D4F0(v13) + 8;
      v28 = 0;
      v27 = v14;
      if ( v12 == 1299478896 )
      {
        v15 = a1[2];
        v16 = *(char *)(*(_QWORD *)(*(_QWORD *)a1 + 48LL) + v15);
        v17 = sub_14083D4F0(v15);
        LODWORD(v33) = v16;
        v32 = v17 + 40;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v27 + 16LL))(v27, &v27);
        v28 = v33;
        v27 = v32;
        v18 = sub_14083D4F0(v33);
        v33 = 0;
        v32 = v18 + 8;
        (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)(v18 + 8) + 16LL))(v18 + 8, &v32);
        sub_140835380(&v29, 1299478896, &v27);
        v14 = v27;
      }
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v27);
    }
  }
  sub_14083DDA0(&v32, &v29);
  v19 = v26;
  v20 = *v26;
  if ( &v32 != v26 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, v26);
    v21 = v32;
    v22 = v33;
    v19[1] = v33;
    *v19 = v21;
    v20 = sub_14083D4F0(v22) + 8;
    v33 = 0;
    v32 = v20;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v20 + 16LL))(v20, &v32);
  sub_140833970(&v29);
  return sub_14083B0A0(&v24);
}
