unsigned __int64 __fastcall sub_143FF45C0(__int64 a1, __int64 *a2, char a3, char a4)
{
  unsigned __int64 result; // rax
  __int64 v8; // rcx
  __int64 v9; // rax
  __int64 v10; // rsi
  unsigned __int64 v11; // r14
  _QWORD *v12; // rbx
  __int64 v13; // r12
  __int64 v14; // rax
  _QWORD *v15; // rax
  __int64 v16; // rbp
  __int64 v17; // r13
  unsigned __int64 v18; // rax
  unsigned __int64 v19; // r15
  unsigned __int64 v20; // rcx
  unsigned __int64 v21; // r15
  _QWORD *v22; // rbp
  unsigned __int64 v23; // rbx
  unsigned __int64 v24; // rcx
  __int64 v25; // rbp
  __int64 v26; // rbp
  bool v27; // al
  char v28; // [rsp+2Eh] [rbp-4Ah]
  char v29; // [rsp+2Fh] [rbp-49h]
  unsigned __int64 v30; // [rsp+30h] [rbp-48h]

  result = *a2;
  if ( *a2 != a2[1] )
    a2[1] = result;
  if ( *(_BYTE *)(a1 + 47) == 1 )
  {
    v8 = *(_QWORD *)(a1 + 48);
    v9 = *(_QWORD *)(v8 + 368);
    if ( v9 != 0 )
    {
      if ( *(_BYTE *)(v8 + 185) == 0 || (v10 = *(_QWORD *)(v9 + 272)) == 0 )
        v10 = *(_QWORD *)(v9 + 264);
    }
    else
    {
      v10 = 0;
    }
    result = *(_QWORD *)(v10 + 1760);
    if ( ((*(_DWORD *)(v10 + 1768) - (_DWORD)result) & 0x7FFF8) != 0 )
    {
      v11 = 0;
      while ( 1 )
      {
        v15 = *(_QWORD **)(result + 8 * v11);
        if ( v15 != nullptr )
        {
          v16 = *v15;
          if ( *v15 != 0
            && sub_141751B70(*a2, a2[1], *v15) == a2[1]
            && (a3 == 0 || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 1704LL))(v16) != 0)
            && (a4 == 0 || (*(__int64 (__fastcall **)(__int64))(*(_QWORD *)v16 + 1720LL))(v16) == 0) )
          {
            break;
          }
        }
LABEL_14:
        ++v11;
        result = *(_QWORD *)(v10 + 1760);
        if ( v11 >= (unsigned __int16)((unsigned int)(*(_DWORD *)(v10 + 1768) - result) >> 3) )
          return result;
      }
      v12 = (_QWORD *)a2[1];
      if ( v12 != (_QWORD *)a2[2] )
      {
        *v12 = v16;
        v13 = *a2;
        v14 = a2[1] + 8;
        a2[1] = v14;
        goto LABEL_13;
      }
      v28 = a3;
      v29 = a4;
      v17 = (__int64)v12 - *a2;
      v18 = v17 >> 3;
      v19 = (unsigned __int64)(v17 >> 3) >> 1;
      v20 = 0x1FFFFFFFFFFFFFFFLL - v19;
      v21 = (v17 >> 3) + v19;
      v30 = (v17 >> 3) + 1;
      if ( v21 <= v30 )
        v21 = v18 + 1;
      if ( v18 > v20 )
        v21 = 0x1FFFFFFFFFFFFFFFLL;
      v13 = sub_1407E4490(qword_141ABD470, 8 * v21);
      *(_QWORD *)(v13 + v17) = v16;
      v22 = (_QWORD *)a2[1];
      sub_141758A00();
      if ( v22 != v12 )
        sub_141758A00();
      v23 = *a2;
      a3 = v28;
      if ( *a2 == 0 )
      {
LABEL_39:
        *a2 = v13;
        v14 = v13 + 8 * v30;
        a2[1] = v14;
        a2[2] = v13 + 8 * v21;
        a4 = v29;
LABEL_13:
        result = v14 - v13;
        if ( result > 0xE8 )
          return result;
        goto LABEL_14;
      }
      v24 = a2[2] - v23;
      if ( v24 == -1 )
      {
        v24 = *(unsigned int *)(v23 - *(unsigned int *)(qword_141ABD470 + 48));
        if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
        {
LABEL_38:
          MEMORY[0x141948990](v23 - *(unsigned int *)(qword_141ABD470 + 48));
          goto LABEL_39;
        }
      }
      else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
      {
        goto LABEL_38;
      }
      v25 = *(_QWORD *)(qword_141ABD470 + 24);
      if ( (*(_QWORD *)(qword_141ABD470 + 32) - v25) >> 3 > v24 )
      {
        v26 = *(_QWORD *)(v25 + 8 * v24);
        if ( v26 != 0 )
        {
          MEMORY[0x1419475D8](v26 + 32, v23 - *(unsigned int *)(v26 + 120));
          v27 = *(_BYTE *)(v26 + 72) != 0 && _InterlockedDecrement((volatile signed __int32 *)(v26 + 64)) != 0;
          if ( !v27 && *(_BYTE *)(v26 + 97) != 0 )
            sub_1412D33C0(v26);
          goto LABEL_39;
        }
      }
      goto LABEL_38;
    }
  }
  return result;
}
