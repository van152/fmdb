// THUNK ALIAS -> sub_143E41260 (jmp:0x140fea8d0->0x143e41260)
__int64 __fastcall sub_143E41260(_QWORD **a1, __int64 *a2)
{
  __int64 **v4; // rax
  __int64 *v5; // rcx
  __int64 v6; // rax
  __int64 v7; // rcx
  __int64 v8; // rdx
  unsigned __int64 v9; // rbx
  __int64 v10; // r12
  __int64 v11; // rsi
  __int64 v12; // r14
  unsigned __int64 v13; // rcx
  __int64 v14; // r8
  __int64 v15; // rcx
  bool v16; // al
  __int64 v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v21; // rdi
  _QWORD **v22; // rax
  __int64 v23; // rcx
  _QWORD *v24; // rax
  __int64 v25; // rsi
  __int64 v26; // rax
  __int64 v27; // [rsp+20h] [rbp-30h]
  __int64 v28; // [rsp+28h] [rbp-28h] BYREF
  __int64 v29; // [rsp+30h] [rbp-20h]
  unsigned __int64 v30; // [rsp+38h] [rbp-18h]
  __int64 v31; // [rsp+40h] [rbp-10h] BYREF
  __int64 v32; // [rsp+48h] [rbp-8h]
  __int64 v33; // [rsp+50h] [rbp+0h]

  v33 = -2;
  sub_1407C9510(&v28);
  v4 = (__int64 **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**a1 + 96LL))(**a1);
  if ( v4 != nullptr )
  {
    v5 = *v4;
    if ( *v4 != nullptr )
    {
      v6 = *v5;
      v7 = v5[1];
      v8 = v7 - v6;
      v9 = (v7 - v6) >> 3;
      v10 = v28;
      if ( (__int64)(v30 - v28) >> 3 >= v9 )
      {
        if ( v7 == v6 )
          goto LABEL_14;
      }
      else
      {
        if ( v8 < 0 )
          sub_1400526C0(v7);
        v11 = v29;
        v12 = sub_1407E4490(qword_141ABD470, v8);
        sub_141758A00();
        if ( v28 != 0 )
        {
          v13 = v30 - v28;
          if ( v30 - v28 == -1 )
            v13 = *(unsigned int *)(v28 - *(unsigned int *)(qword_141ABD470 + 48));
          if ( *(_BYTE *)(qword_141ABD470 + 52) != 0
            && (v14 = *(_QWORD *)(qword_141ABD470 + 24), (*(_QWORD *)(qword_141ABD470 + 32) - v14) >> 3 > v13)
            && (v15 = *(_QWORD *)(v14 + 8 * v13)) != 0 )
          {
            v27 = v15;
            MEMORY[0x1419475D8](v15 + 32, v28 - *(unsigned int *)(v15 + 120));
            v16 = *(_BYTE *)(v27 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v27 + 64)) != 0;
            if ( !v16 && *(_BYTE *)(v27 + 97) != 0 )
              sub_1412D33C0(v27);
          }
          else
          {
            MEMORY[0x141948990](v28 - *(unsigned int *)(qword_141ABD470 + 48));
          }
        }
        v28 = v12;
        v29 = v12 + v11 - v10;
        v30 = v12 + 8 * v9;
      }
      v21 = 0;
      do
      {
        v22 = (_QWORD **)(*(__int64 (__fastcall **)(_QWORD))(*(_QWORD *)**a1 + 96LL))(**a1);
        if ( v22 != nullptr )
        {
          v24 = *v22;
          if ( v24 != nullptr )
          {
            v25 = *(_QWORD *)(*v24 + 8 * v21);
            if ( v25 != 0 )
            {
              v26 = sub_14083D4F0(v23);
              v32 = 0;
              v31 = v26 + 8;
              sub_140FEA6A0(v25, &v31);
              sub_14083B5F0(&v28, &v31);
              (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v31 + 16LL))(v31, &v31);
            }
          }
        }
        ++v21;
      }
      while ( v9 != v21 );
    }
  }
LABEL_14:
  sub_14083DB80(&v31, &v28);
  v17 = *a2;
  if ( &v31 != a2 )
  {
    (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, a2);
    v18 = v31;
    v19 = v32;
    a2[1] = v32;
    *a2 = v18;
    v17 = sub_14083D4F0(v19) + 8;
    v32 = 0;
    v31 = v17;
  }
  (*(void (__fastcall **)(__int64, __int64 *))(*(_QWORD *)v17 + 16LL))(v17, &v31);
  return sub_14083B0A0(&v28);
}
