__int64 __fastcall sub_141567790(_QWORD *a1, int a2, unsigned __int64 *a3)
{
  unsigned int v4; // esi
  __int64 v5; // rax
  unsigned __int64 v6; // rcx
  int v7; // ebx
  __int64 v8; // rax
  unsigned __int64 v9; // rax
  unsigned __int64 v10; // rcx
  __int64 v11; // rax
  unsigned __int64 v12; // rcx
  int v13; // ebx
  unsigned __int64 v14; // rax
  unsigned __int64 v15; // rcx
  __int64 v16; // rcx
  int v17; // eax
  int v18; // ecx
  __int16 *v19; // rax
  int v20; // ebx
  unsigned __int64 v21; // rax
  unsigned __int64 v22; // rcx
  char *v23; // rax
  int v24; // ebx
  unsigned __int64 v25; // rax
  unsigned __int64 v26; // rcx
  __int64 v27; // rax
  unsigned __int64 v28; // rcx
  int v29; // ebx
  unsigned __int64 v30; // rax
  unsigned __int64 v31; // rcx
  __int64 v32; // rax
  unsigned __int64 v33; // rcx
  int v34; // ebx
  unsigned __int64 v35; // rax
  unsigned __int64 v36; // rcx
  unsigned __int64 v38; // [rsp+20h] [rbp-10h] BYREF
  unsigned __int64 v39; // [rsp+28h] [rbp-8h]
  __int64 v40; // [rsp+30h] [rbp+0h]

  v40 = -2;
  v4 = 0;
  if ( a2 <= 1886679856 )
  {
    switch ( a2 )
    {
      case 1734438193:
        v23 = (char *)a1[8];
        LOBYTE(v4) = 1;
        if ( (char *)a1[9] != v23 )
        {
          v24 = *v23;
          v8 = sub_14083D4F0(a1) + 40;
          LODWORD(v39) = v24;
          v38 = v8;
          if ( &v38 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v25 = v38;
            v26 = v39;
            a3[1] = v39;
            *a3 = v25;
            v8 = sub_14083D4F0(v26) + 8;
            v39 = 0;
            v38 = v8;
          }
          goto LABEL_36;
        }
        break;
      case 1734438194:
        v27 = a1[8];
        v28 = a1[9] - v27;
        LOBYTE(v4) = 1;
        if ( v28 >= 2 )
        {
          v29 = *(char *)(v27 + 1);
          v8 = sub_14083D4F0(v28) + 40;
          LODWORD(v39) = v29;
          v38 = v8;
          if ( &v38 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v30 = v38;
            v31 = v39;
            a3[1] = v39;
            *a3 = v30;
            v8 = sub_14083D4F0(v31) + 8;
            v39 = 0;
            v38 = v8;
          }
          goto LABEL_36;
        }
        break;
      case 1734438195:
        v11 = a1[8];
        v12 = a1[9] - v11;
        LOBYTE(v4) = 1;
        if ( v12 >= 3 )
        {
          v13 = *(char *)(v11 + 2);
          v8 = sub_14083D4F0(v12) + 40;
          LODWORD(v39) = v13;
          v38 = v8;
          if ( &v38 != a3 )
          {
            (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
            v14 = v38;
            v15 = v39;
            a3[1] = v39;
            *a3 = v14;
            v8 = sub_14083D4F0(v15) + 8;
            v39 = 0;
            v38 = v8;
          }
          goto LABEL_36;
        }
        break;
      default:
        break;
    }
  }
  else if ( a2 > 1886679858 )
  {
    if ( a2 == 1886679859 )
    {
      v32 = a1[5];
      v33 = a1[6] - v32;
      LOBYTE(v4) = 1;
      if ( v33 >= 5 )
      {
        v34 = *(__int16 *)(v32 + 4);
        v8 = sub_14083D4F0(v33) + 40;
        LODWORD(v39) = v34;
        v38 = v8;
        if ( &v38 != a3 )
        {
          (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
          v35 = v38;
          v36 = v39;
          a3[1] = v39;
          *a3 = v35;
          v8 = sub_14083D4F0(v36) + 8;
          v39 = 0;
          v38 = v8;
        }
        goto LABEL_36;
      }
    }
    else if ( a2 == 1952801133 )
    {
      v16 = a1[3];
      if ( v16 != 0 )
      {
        v17 = *(_DWORD *)(v16 + 12);
        v18 = *(_DWORD *)(v16 + 16);
        if ( v18 == 0 )
          v18 = v17;
      }
      else
      {
        v17 = -1;
        v18 = -1;
      }
      v38 = __PAIR64__(v18, v17);
      sub_140FE72B0(&v38, 1416914273, a3);
      LOBYTE(v4) = 1;
    }
  }
  else if ( a2 == 1886679857 )
  {
    v19 = (__int16 *)a1[5];
    LOBYTE(v4) = 1;
    if ( (__int16 *)a1[6] != v19 )
    {
      v20 = *v19;
      v8 = sub_14083D4F0(a1) + 40;
      LODWORD(v39) = v20;
      v38 = v8;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v21 = v38;
        v22 = v39;
        a3[1] = v39;
        *a3 = v21;
        v8 = sub_14083D4F0(v22) + 8;
        v39 = 0;
        v38 = v8;
      }
      goto LABEL_36;
    }
  }
  else
  {
    v5 = a1[5];
    v6 = a1[6] - v5;
    LOBYTE(v4) = 1;
    if ( v6 >= 3 )
    {
      v7 = *(__int16 *)(v5 + 2);
      v8 = sub_14083D4F0(v6) + 40;
      LODWORD(v39) = v7;
      v38 = v8;
      if ( &v38 != a3 )
      {
        (*(void (__fastcall **)(unsigned __int64, unsigned __int64 *))(*(_QWORD *)*a3 + 16LL))(*a3, a3);
        v9 = v38;
        v10 = v39;
        a3[1] = v39;
        *a3 = v9;
        v8 = sub_14083D4F0(v10) + 8;
        v39 = 0;
        v38 = v8;
      }
LABEL_36:
      (*(void (__fastcall **)(__int64, unsigned __int64 *))(*(_QWORD *)v8 + 16LL))(v8, &v38);
    }
  }
  return v4;
}
