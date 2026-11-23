__int64 __fastcall sub_143EE0FD0(__int64 a1, __int64 *a2)
{
  __int64 v4; // rdi
  __int64 v5; // rbx
  unsigned __int64 v6; // rsi
  __int64 v7; // r13
  __int64 i; // rdi
  __int64 *v9; // rdx
  unsigned int v10; // esi
  __int64 v11; // rcx
  __int64 v12; // rax
  __int64 *v13; // rdi
  __int64 v14; // rcx
  __int64 v15; // rax
  __int64 v16; // rcx
  __int64 v18; // [rsp+28h] [rbp-48h] BYREF
  __int64 v19; // [rsp+30h] [rbp-40h]
  __int64 *v20; // [rsp+40h] [rbp-30h]
  __int64 v21[3]; // [rsp+48h] [rbp-28h] BYREF
  __int64 v22; // [rsp+60h] [rbp-10h] BYREF
  __int64 v23; // [rsp+68h] [rbp-8h]
  __int64 v24; // [rsp+70h] [rbp+0h]

  v24 = -2;
  sub_1407C9510(&v18);
  sub_14144C820(&v18);
  sub_1407C9510(v21);
  v4 = v18;
  v5 = v19;
  v6 = (v19 - v18) >> 3;
  if ( (v21[2] - v21[0]) >> 4 < v6 )
  {
    if ( (unsigned __int64)(v19 - v18) >= 0x7FFFFFFFFFFFFFF9LL )
      sub_1400526C0(0x7FFFFFFFFFFFFFF9LL);
    sub_140837DD0(v21, (v19 - v18) >> 3);
  }
  v20 = a2;
  if ( v5 != v4 )
  {
    v7 = 1;
    if ( v6 >= 2 )
      v7 = v6;
    for ( i = 0; i != v7; ++i )
    {
      v9 = *(__int64 **)(v18 + 8 * i);
      if ( v9 == nullptr )
        v9 = &qword_141B5A4A0;
      v10 = (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)*v9 + 80LL))(*v9);
      v12 = sub_14083D4F0(v11);
      v23 = 0;
      v22 = v12 + 8;
      if ( (unsigned __int8)sub_14144CB60(a1, v10, &v22) != 0 )
        sub_140835380(v21, v10, &v22);
      (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v22 + 16LL))(v22, &v22);
    }
  }
  sub_14083DDA0(&v22, v21);
  v13 = v20;
  v14 = *v20;
  if ( &v22 != v20 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, v20);
    v15 = v22;
    v16 = v23;
    v13[1] = v23;
    *v13 = v15;
    v14 = sub_14083D4F0(v16) + 8;
    v23 = 0;
    v22 = v14;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v14 + 16LL))(v14, &v22);
  sub_140833970(v21);
  return sub_14083B0A0(&v18);
}
