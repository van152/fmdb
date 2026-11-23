_DWORD *__fastcall sub_141074100(_DWORD *a1, _QWORD *a2, _QWORD *a3)
{
  _QWORD *v4; // rbp
  __int64 v6; // rdi
  __int64 v7; // r14
  __int64 v8; // rbx
  unsigned __int64 v9; // r15
  __int64 v10; // rcx
  __int64 v11; // rcx
  _QWORD *v12; // r13
  __int64 v13; // rbp
  char *v14; // rax
  char *v15; // rsi
  __int64 v16; // r13
  __int64 v17; // r15
  unsigned __int64 v18; // rsi
  unsigned __int64 v19; // rbp
  unsigned __int64 v20; // rbx
  __int64 v21; // rcx
  __int64 v22; // rcx
  __int64 v23; // r14
  char *v24; // rax
  char *v25; // rdi
  __int64 v26; // rsi
  __int64 v27; // rbx
  unsigned int v29; // [rsp+2Ch] [rbp-6Ch] BYREF
  __int64 v30; // [rsp+30h] [rbp-68h] BYREF
  int v31; // [rsp+38h] [rbp-60h]
  _DWORD *v32; // [rsp+40h] [rbp-58h]
  _QWORD *v33; // [rsp+48h] [rbp-50h]
  unsigned __int64 v34; // [rsp+50h] [rbp-48h]

  v4 = a2;
  v29 = 0;
  (*(void (__fastcall **)(_QWORD, unsigned int *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, &v29, 4);
  v6 = v29;
  if ( qword_141AA7808 <= (unsigned __int64)v29 )
  {
LABEL_38:
    *a1 = 1;
    return a1;
  }
  v32 = a1;
  v7 = *a3;
  if ( 0xAAAAAAAAAAAAAAABuLL * ((__int64)(a3[2] - *a3) >> 2) < v29 )
  {
    v8 = a3[1];
    v9 = 12LL * v29;
    if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
      && (v10 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v10) >> 3 > v9)
      && (v11 = *(_QWORD *)(v10 + 96LL * v29)) != 0 )
    {
      v12 = v4;
      v13 = *(unsigned int *)(v11 + 88);
      v14 = (char *)sub_1407E58C0(v11, *(unsigned int *)(v11 + 80));
    }
    else
    {
      v12 = v4;
      v13 = *(unsigned int *)(qword_141ABE200 + 48);
      v14 = (char *)sub_141601260((unsigned int)(v13 + v9), 4096);
    }
    v15 = v14;
    if ( v13 != 0 )
    {
      *(_DWORD *)v14 = v9;
      v15 = &v14[v13];
    }
    v4 = v12;
    sub_141758A00();
    if ( *a3 != 0 )
      sub_1407E6420(qword_141ABE200, *a3, a3[2] - *a3);
    *a3 = v15;
    a3[1] = &v15[v8 - v7];
    a3[2] = &v15[12 * v6];
    LODWORD(v6) = v29;
  }
  if ( (_DWORD)v6 != 0 )
  {
    v16 = 0;
    v33 = v4;
    while ( 1 )
    {
      v30 = 0xFF63FF00000000LL;
      v31 = 0;
      if ( (unsigned __int8)sub_140D893E0(&v30, v4) == 0 )
        break;
      if ( *(_DWORD *)(*v4 + 16LL) == 0 )
      {
        v17 = a3[1];
        if ( v17 == a3[2] )
        {
          v18 = 0xAAAAAAAAAAAAAAABuLL * ((v17 - *a3) >> 2);
          v19 = v18 + (v18 >> 1);
          v34 = v18 + 1;
          if ( v19 <= v18 + 1 )
            v19 = v18 + 1;
          if ( v18 > 0x1555555555555555LL - (v18 >> 1) )
            v19 = 0x1555555555555555LL;
          v20 = 12 * v19;
          if ( *(_BYTE *)(qword_141ABE200 + 52) != 0
            && (v21 = *(_QWORD *)(qword_141ABE200 + 24), (*(_QWORD *)(qword_141ABE200 + 32) - v21) >> 3 > v20)
            && (v22 = *(_QWORD *)(v21 + 96 * v19)) != 0 )
          {
            v23 = *(unsigned int *)(v22 + 88);
            v24 = (char *)sub_1407E58C0(v22, *(unsigned int *)(v22 + 80));
          }
          else
          {
            v23 = *(unsigned int *)(qword_141ABE200 + 48);
            v24 = (char *)sub_141601260((unsigned int)(v23 + v20), 4096);
          }
          v25 = v24;
          if ( v23 != 0 )
          {
            *(_DWORD *)v24 = v20;
            v25 = &v24[v23];
          }
          v26 = 3 * v18;
          *(_DWORD *)&v25[4 * v26 + 8] = v31;
          *(_QWORD *)&v25[4 * v26] = v30;
          v27 = a3[1];
          sub_141758A00();
          if ( v27 != v17 )
            sub_141758A00();
          if ( *a3 != 0 )
            sub_1407E6420(qword_141ABE200, *a3, a3[2] - *a3);
          *a3 = v25;
          a3[1] = &v25[12 * v34];
          a3[2] = &v25[12 * v19];
          v4 = v33;
        }
        else
        {
          *(_DWORD *)(v17 + 8) = v31;
          *(_QWORD *)v17 = v30;
          a3[1] += 12LL;
        }
        if ( ++v16 < (unsigned __int64)v29 )
          continue;
      }
      goto LABEL_36;
    }
    a1 = v32;
    goto LABEL_38;
  }
LABEL_36:
  a1 = v32;
  *v32 = *(_DWORD *)(*v4 + 16LL);
  return a1;
}
