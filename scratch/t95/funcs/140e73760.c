__int64 __fastcall sub_140E73760(_QWORD *a1)
{
  _QWORD *v1; // r15
  __int64 v2; // r8
  __int64 v3; // r8
  unsigned __int64 *v4; // r13
  unsigned __int64 *v5; // r14
  unsigned __int64 *v6; // r12
  __int64 v7; // rbp
  unsigned __int64 v8; // rbx
  __int64 v9; // rax
  unsigned __int64 *v10; // rsi
  unsigned __int64 v11; // r14
  __int64 v12; // r15
  unsigned __int64 v13; // rbx
  unsigned __int64 *v14; // rdi
  unsigned __int64 *v15; // rcx
  __int64 v16; // rdx
  bool v17; // cf
  unsigned __int64 v18; // r15
  unsigned __int64 v19; // rax
  unsigned __int64 v20; // rcx
  unsigned __int64 v21; // rsi
  __int64 v22; // rax
  unsigned __int64 v23; // rcx
  _QWORD *v24; // rax
  unsigned __int64 v25; // rdi
  __int64 v26; // rax
  _QWORD *v27; // r12
  _QWORD *v28; // rbp
  __int64 v29; // rsi
  unsigned __int64 v30; // r15
  __int64 v31; // rdi
  unsigned __int64 v32; // rbp
  unsigned __int64 *v33; // rsi
  unsigned __int64 *v34; // rdx
  __int64 v35; // rcx
  unsigned __int64 v36; // rdi
  unsigned __int64 v37; // r14
  __int64 v38; // rax
  __int64 v41; // [rsp+30h] [rbp-68h]
  _QWORD *v42; // [rsp+30h] [rbp-68h]
  unsigned __int64 v43; // [rsp+38h] [rbp-60h]
  unsigned __int64 *v44; // [rsp+38h] [rbp-60h]
  _QWORD *v45; // [rsp+40h] [rbp-58h]
  _QWORD *v46; // [rsp+48h] [rbp-50h]
  unsigned __int64 v47; // [rsp+50h] [rbp-48h]

  v1 = a1;
  v2 = a1[10] - a1[9];
  if ( v2 != 0 )
  {
    v3 = v2 >> 4;
    v4 = nullptr;
    v5 = nullptr;
    v6 = nullptr;
    v7 = 0;
    v41 = v3;
    while ( 1 )
    {
      v9 = v1[9];
      if ( *(_BYTE *)(v9 + 16 * v7 + 11) != 127 )
      {
        v8 = (unsigned __int64)v6;
        goto LABEL_4;
      }
      v10 = v5;
      if ( *(_BYTE *)(v9 + 16 * v7 + 10) == 3 )
        v11 = *(_QWORD *)(v9 + 16 * v7);
      else
        v11 = 0;
      v12 = (char *)v4 - (char *)v6;
      if ( (char *)v4 - (char *)v6 <= 0 )
      {
        v14 = v6;
        if ( v6 == v4 )
          goto LABEL_19;
      }
      else
      {
        v13 = (unsigned __int64)v12 >> 3;
        v14 = v6;
        do
        {
          v15 = v14;
          v16 = v13 + ~(v13 >> 1);
          v17 = v14[v13 >> 1] < v11;
          v14 += (v13 >> 1) + 1;
          if ( !v17 )
          {
            v14 = v15;
            v16 = v13 >> 1;
          }
          v13 = v16;
        }
        while ( v16 > 0 );
        if ( v14 == v4 )
        {
LABEL_19:
          if ( v4 != v10 )
          {
            *v4++ = v11;
            goto LABEL_21;
          }
          goto LABEL_22;
        }
      }
      if ( v11 >= *v14 )
        goto LABEL_21;
      if ( v4 != v10 )
      {
        *v4 = *(v4 - 1);
        sub_141758A00();
        v3 = v41;
        *v14 = v11;
        ++v4;
LABEL_21:
        v8 = (unsigned __int64)v6;
        v5 = v10;
        v1 = a1;
        goto LABEL_4;
      }
LABEL_22:
      v18 = (v12 >> 3) + 1;
      v43 = (char *)v10 - (char *)v6;
      v19 = v10 - v6;
      v20 = 0x1FFFFFFFFFFFFFFFLL - (v19 >> 1);
      v21 = v19 + (v19 >> 1);
      if ( v21 <= v18 )
        v21 = v18;
      if ( v19 > v20 )
        v21 = 0x1FFFFFFFFFFFFFFFLL;
      if ( v21 > 0x1FFFFFFFFFFFFFFFLL )
LABEL_91:
        sub_1400DAC30(v20);
      v20 = 8 * v21;
      if ( v21 < 0x200 )
      {
        if ( v21 != 0 )
          v8 = sub_141750CC0(v20);
        else
          v8 = 0;
      }
      else
      {
        if ( v21 >= 0x1FFFFFFFFFFFFFFCLL )
          goto LABEL_91;
        v22 = sub_141750CC0(v20 + 39);
        v8 = (v22 + 39) & 0xFFFFFFFFFFFFFFE0uLL;
        *(_QWORD *)(v8 - 8) = v22;
      }
      *(_QWORD *)(v8 + 8 * (v14 - v6)) = v11;
      sub_141758A00();
      if ( v14 != v4 )
        sub_141758A00();
      if ( v6 != nullptr )
      {
        if ( v43 >= 0x1000 )
        {
          if ( (unsigned __int64)v6 - *(v6 - 1) - 8 >= 0x20 )
            goto LABEL_92;
          v6 = (unsigned __int64 *)*(v6 - 1);
        }
        sub_141750D04(v6);
      }
      v4 = (unsigned __int64 *)(v8 + 8 * v18);
      v5 = (unsigned __int64 *)(v8 + 8 * v21);
      v1 = a1;
      v3 = v41;
LABEL_4:
      ++v7;
      v6 = (unsigned __int64 *)v8;
      if ( v7 == v3 )
        goto LABEL_42;
    }
  }
  v4 = nullptr;
  v5 = nullptr;
  v8 = 0;
LABEL_42:
  v24 = (_QWORD *)v1[3];
  v45 = (_QWORD *)v1[4];
  if ( v24 != v45 )
  {
    while ( 1 )
    {
      v46 = v24;
      v26 = *v24;
      if ( v26 != 0 )
      {
        v27 = *(_QWORD **)(v26 + 56);
        v28 = *(_QWORD **)(v26 + 64);
        if ( v27 != v28 )
          break;
      }
      v25 = v8;
LABEL_49:
      v24 = v46 + 1;
      v8 = v25;
      if ( v46 + 1 == v45 )
        goto LABEL_44;
    }
    v42 = *(_QWORD **)(v26 + 64);
    while ( 1 )
    {
      v29 = *v27;
      if ( (*(unsigned __int8 (__fastcall **)(_QWORD, _QWORD *))(*(_QWORD *)*v27 + 736LL))(*v27, v1) == 0 )
      {
        v25 = v8;
        goto LABEL_54;
      }
      v30 = v29 + *(int *)(*(_QWORD *)(v29 + 8) + 4LL) + 8;
      v31 = (__int64)v4 - v8;
      if ( (__int64)((__int64)v4 - v8) <= 0 )
      {
        v33 = (unsigned __int64 *)v8;
        if ( (unsigned __int64 *)v8 == v4 )
          goto LABEL_66;
      }
      else
      {
        v32 = (unsigned __int64)v31 >> 3;
        v33 = (unsigned __int64 *)v8;
        do
        {
          v34 = v33;
          v35 = v32 + ~(v32 >> 1);
          v17 = v33[v32 >> 1] < v30;
          v33 += (v32 >> 1) + 1;
          if ( !v17 )
          {
            v33 = v34;
            v35 = v32 >> 1;
          }
          v32 = v35;
        }
        while ( v35 > 0 );
        if ( v33 == v4 )
        {
LABEL_66:
          if ( v4 != v5 )
          {
            *v4++ = v30;
            goto LABEL_68;
          }
          goto LABEL_69;
        }
      }
      if ( v30 >= *v33 )
        goto LABEL_68;
      if ( v4 != v5 )
      {
        *v4 = *(v4 - 1);
        sub_141758A00();
        *v33 = v30;
        ++v4;
LABEL_68:
        v25 = v8;
        v1 = a1;
        v28 = v42;
        goto LABEL_54;
      }
LABEL_69:
      v44 = v5;
      v36 = v31 >> 3;
      v20 = 0x1FFFFFFFFFFFFFFFLL;
      v37 = v36 + (v36 >> 1);
      if ( v37 <= v36 + 1 )
        v37 = v36 + 1;
      if ( v36 > 0x1FFFFFFFFFFFFFFFLL - (v36 >> 1) )
        v37 = 0x1FFFFFFFFFFFFFFFLL;
      if ( v37 > 0x1FFFFFFFFFFFFFFFLL )
        goto LABEL_91;
      v20 = 8 * v37;
      v47 = v36 + 1;
      if ( v37 < 0x200 )
      {
        if ( v37 != 0 )
          v25 = sub_141750CC0(v20);
        else
          v25 = 0;
      }
      else
      {
        if ( v37 >= 0x1FFFFFFFFFFFFFFCLL )
          goto LABEL_91;
        v38 = sub_141750CC0(v20 + 39);
        v25 = (v38 + 39) & 0xFFFFFFFFFFFFFFE0uLL;
        *(_QWORD *)(v25 - 8) = v38;
      }
      *(_QWORD *)(v25 + 8 * ((__int64)((__int64)v33 - v8) >> 3)) = v30;
      sub_141758A00();
      if ( v33 != v4 )
        sub_141758A00();
      v1 = a1;
      v28 = v42;
      if ( v8 != 0 )
      {
        if ( (unsigned __int64)v44 - v8 >= 0x1000 )
        {
          if ( v8 - 8 - *(_QWORD *)(v8 - 8) >= 0x20 )
            goto LABEL_92;
          v8 = *(_QWORD *)(v8 - 8);
        }
        sub_141750D04(v8);
      }
      v4 = (unsigned __int64 *)(v25 + 8 * v47);
      v5 = (unsigned __int64 *)(v25 + 8 * v37);
LABEL_54:
      ++v27;
      v8 = v25;
      if ( v27 == v28 )
        goto LABEL_49;
    }
  }
  v25 = v8;
LABEL_44:
  if ( v25 != 0 )
  {
    if ( (unsigned __int64)v5 - v25 < 0x1000 )
    {
      v23 = v25;
    }
    else
    {
      v23 = *(_QWORD *)(v25 - 8);
      if ( v25 - 8 - v23 >= 0x20 )
LABEL_92:
        MEMORY[0x1419488E8](v23);
    }
    sub_141750D04(v23);
  }
  return (unsigned int)((_DWORD)v4 - v25) >> 3;
}
