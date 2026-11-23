__int64 __fastcall sub_141540880(__int64 a1, int a2, unsigned int *a3)
{
  _BYTE *v5; // rsi
  __int64 v6; // rax
  __int64 v7; // r8
  __int64 v8; // rcx
  __int64 v9; // rcx
  __int64 v10; // rax
  __int64 v11; // r8
  __int64 v12; // rcx
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // r9
  __int64 v16; // rcx
  __int64 v17; // rcx
  __int64 v18; // rax
  __int64 v19; // rcx
  __int64 v20; // rcx
  __int64 v21; // rax
  __int64 v22; // rcx
  __int64 v23; // rcx
  __int64 v24; // rax
  __int64 v25; // rcx
  __int64 v26; // rcx
  __int64 v27; // rax
  __int64 v28; // rcx
  __int64 v29; // rcx
  __int64 v30; // rax
  __int64 v31; // r8
  __int64 v32; // rcx
  __int64 v33; // rcx
  __int64 v34; // rax
  __int64 v35; // rcx
  __int64 v36; // rcx
  __int64 v37; // rax
  __int64 v38; // rcx
  __int64 v39; // rcx
  __int64 v40; // rax
  __int64 v41; // rcx
  __int64 v42; // rcx
  unsigned int v43; // eax
  __int64 v44; // rdx
  __int64 v45; // rdx
  int v46; // eax
  int v47; // eax
  _QWORD *v48; // rbx
  __int64 v49; // rdx
  unsigned __int64 v50; // rcx
  __int64 v51; // rbx
  __int64 v52; // rbx
  _BYTE *v54; // [rsp+20h] [rbp-58h] BYREF
  _QWORD *v55; // [rsp+28h] [rbp-50h]
  _BYTE v56[8]; // [rsp+30h] [rbp-48h] BYREF
  _QWORD v57[2]; // [rsp+38h] [rbp-40h] BYREF
  __int64 v58; // [rsp+48h] [rbp-30h]

  LODWORD(v5) = 0;
  if ( a2 > 1768846187 )
  {
    if ( a2 > 1886151780 )
    {
      if ( a2 != 1886151781 )
      {
        if ( a2 == 1886155372 )
        {
          v40 = sub_140FE84D0();
          if ( v40 == 0
            || (v41 = *(_QWORD *)(a1 + 24)) == 0
            || ((v7 = 0, *(_BYTE *)(v41 + 47) != 0) ? (v42 = 0) : (v42 = *(_QWORD *)(v41 + 48)), v40 != v42) )
          {
            LOBYTE(v7) = 1;
          }
          v44 = a1;
        }
        else
        {
          if ( a2 != 1886155378 )
            return (unsigned int)v5;
          v14 = sub_140FE84D0();
          if ( v14 != 0
            && (v16 = *(_QWORD *)(a1 + 24)) != 0
            && (*(_BYTE *)(v16 + 47) != 0 ? (v17 = 0) : (v17 = *(_QWORD *)(v16 + 48)), v14 == v17) )
          {
            LOBYTE(v7) = 1;
          }
          else
          {
            v7 = 0;
          }
          v44 = a1;
        }
        LOBYTE(v15) = 1;
        goto LABEL_114;
      }
      v37 = sub_140FE84D0();
      if ( v37 == 0
        || (v38 = *(_QWORD *)(a1 + 24)) == 0
        || ((v7 = 0, *(_BYTE *)(v38 + 47) != 0) ? (v39 = 0) : (v39 = *(_QWORD *)(v38 + 48)), v37 != v39) )
      {
        LOBYTE(v7) = 1;
      }
      v44 = a1;
    }
    else
    {
      if ( a2 == 1768846188 )
      {
        v24 = sub_140FE84D0();
        if ( v24 != 0
          && (v25 = *(_QWORD *)(a1 + 24)) != 0
          && (*(_BYTE *)(v25 + 47) != 0 ? (v26 = 0) : (v26 = *(_QWORD *)(v25 + 48)), v24 == v26) )
        {
          LOBYTE(v11) = 1;
        }
        else
        {
          v11 = 0;
        }
        v45 = a1;
LABEL_90:
        sub_141732E30(v56, v45, v11);
        v54 = v56;
        v55 = v57;
        v47 = sub_1415437F0(&v54, a3);
        goto LABEL_115;
      }
      if ( a2 == 1869902957 )
      {
        v27 = sub_140FE84D0();
        if ( v27 != 0
          && (v28 = *(_QWORD *)(a1 + 24)) != 0
          && (*(_BYTE *)(v28 + 47) != 0 ? (v29 = 0) : (v29 = *(_QWORD *)(v28 + 48)), v27 == v29) )
        {
          v48 = (_QWORD *)(a1 + 32);
        }
        else
        {
          v48 = (_QWORD *)(a1 + 24);
        }
        v5 = (_BYTE *)qword_141B5FE40;
        sub_140FE7960(v56, a3, 1416914273);
        *v48 = sub_140FA3700(v5, v56);
        LOBYTE(v5) = 1;
        return (unsigned int)v5;
      }
      if ( a2 != 1886151026 )
        return (unsigned int)v5;
      v6 = sub_140FE84D0();
      if ( v6 != 0
        && (v8 = *(_QWORD *)(a1 + 24)) != 0
        && (*(_BYTE *)(v8 + 47) != 0 ? (v9 = 0) : (v9 = *(_QWORD *)(v8 + 48)), v6 == v9) )
      {
        LOBYTE(v7) = 1;
      }
      else
      {
        v7 = 0;
      }
      v44 = a1;
    }
    v15 = 0;
LABEL_114:
    sub_141731FC0(v56, v44, v7, v15);
    v54 = v56;
    v55 = v57;
    v47 = sub_1415425F0(&v54, a3);
    goto LABEL_115;
  }
  if ( a2 <= 1685217643 )
  {
    if ( a2 == 1634495602 )
    {
      v18 = sub_140FE84D0();
      if ( v18 != 0 )
      {
        v19 = *(_QWORD *)(a1 + 24);
        if ( v19 != 0 )
        {
          v20 = *(_BYTE *)(v19 + 47) != 0 ? 0LL : *(_QWORD *)(v19 + 48);
          if ( v18 == v20 )
          {
LABEL_84:
            v46 = -(*(int (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
            goto LABEL_85;
          }
        }
      }
    }
    else
    {
      if ( a2 != 1634495603 )
      {
        if ( a2 == 1684108389 )
        {
          if ( dword_141B5C8D0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer
                                             + (unsigned int)TlsIndex)
                                           + 4LL) )
          {
            sub_141750E08(&dword_141B5C8D0);
            if ( dword_141B5C8D0 == -1 )
            {
              sub_140DBC9B0(&qword_141B5C8A0);
              sub_141751048(sub_140DBCA10);
              sub_141750EA0(&dword_141B5C8D0);
            }
          }
          if ( *(__int64 **)a3 == &qword_141B5C8A0 )
          {
            v43 = a3[2];
            WORD1(v54) = v43 >> 17;
            LOWORD(v54) = (v43 >> 8) & 0x1FF | ((_WORD)v43 << 9);
          }
          else if ( (*(unsigned __int8 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 8LL))(
                      *(_QWORD *)a3,
                      a3) == 27 )
          {
            v5 = v56;
            (*(void (__fastcall **)(_QWORD, _BYTE *, unsigned int *))(**(_QWORD **)a3 + 160LL))(*(_QWORD *)a3, v56, a3);
            sub_1413CA830(&v54, v56);
          }
          else
          {
            LODWORD(v54) = 124518401;
          }
          *(_DWORD *)(a1 + 40) = (_DWORD)v54;
          LOBYTE(v5) = 1;
        }
        return (unsigned int)v5;
      }
      v21 = sub_140FE84D0();
      if ( v21 == 0 )
        goto LABEL_84;
      v22 = *(_QWORD *)(a1 + 24);
      if ( v22 == 0 )
        goto LABEL_84;
      v23 = *(_BYTE *)(v22 + 47) != 0 ? 0LL : *(_QWORD *)(v22 + 48);
      if ( v21 != v23 )
        goto LABEL_84;
    }
    v46 = (*(__int64 (__fastcall **)(_QWORD, unsigned int *))(**(_QWORD **)a3 + 64LL))(*(_QWORD *)a3, a3);
LABEL_85:
    *(_DWORD *)(a1 + 44) = v46;
    LOBYTE(v5) = 1;
    return (unsigned int)v5;
  }
  switch ( a2 )
  {
    case 1685217644:
      v30 = sub_140FE84D0();
      if ( v30 != 0
        && (v32 = *(_QWORD *)(a1 + 24)) != 0
        && (*(_BYTE *)(v32 + 47) != 0 ? (v33 = 0) : (v33 = *(_QWORD *)(v32 + 48)), v30 == v33) )
      {
        LOBYTE(v31) = 1;
      }
      else
      {
        v31 = 0;
      }
      v49 = a1;
      break;
    case 1701077356:
      v34 = sub_140FE84D0();
      if ( v34 == 0
        || (v35 = *(_QWORD *)(a1 + 24)) == 0
        || ((v31 = 0, *(_BYTE *)(v35 + 47) != 0) ? (v36 = 0) : (v36 = *(_QWORD *)(v35 + 48)), v34 != v36) )
      {
        LOBYTE(v31) = 1;
      }
      v49 = a1;
      break;
    case 1702390131:
      v10 = sub_140FE84D0();
      if ( v10 == 0
        || (v12 = *(_QWORD *)(a1 + 24)) == 0
        || ((v11 = 0, *(_BYTE *)(v12 + 47) != 0) ? (v13 = 0) : (v13 = *(_QWORD *)(v12 + 48)), v10 != v13) )
      {
        LOBYTE(v11) = 1;
      }
      v45 = a1;
      goto LABEL_90;
    default:
      return (unsigned int)v5;
  }
  sub_141732860(v56, v49, v31);
  v54 = v56;
  v55 = v57;
  v47 = sub_141542EB0(&v54, a3);
LABEL_115:
  LODWORD(v5) = v47;
  if ( v57[0] == 0 )
    return (unsigned int)v5;
  v50 = v58 - v57[0];
  if ( v58 - v57[0] == -1 )
  {
    v50 = *(unsigned int *)(v57[0] - *(unsigned int *)(qword_141ABD470 + 48));
    if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
    {
LABEL_125:
      MEMORY[0x141948990](v57[0] - *(unsigned int *)(qword_141ABD470 + 48));
      return (unsigned int)v5;
    }
  }
  else if ( *(_BYTE *)(qword_141ABD470 + 52) == 0 )
  {
    goto LABEL_125;
  }
  v51 = *(_QWORD *)(qword_141ABD470 + 24);
  if ( (*(_QWORD *)(qword_141ABD470 + 32) - v51) >> 3 <= v50 )
    goto LABEL_125;
  v52 = *(_QWORD *)(v51 + 8 * v50);
  if ( v52 == 0 )
    goto LABEL_125;
  MEMORY[0x1419475D8](v52 + 32, v57[0] - *(unsigned int *)(v52 + 120));
  if ( (*(_BYTE *)(v52 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v52 + 64)) == 0)
    && *(_BYTE *)(v52 + 97) != 0 )
  {
    sub_1412D33C0(v52);
  }
  return (unsigned int)v5;
}
