__int64 __fastcall sub_1411DC000(_QWORD *a1, __int64 a2, char a3, char a4, unsigned __int8 a5, unsigned __int8 a6)
{
  __int64 v7; // rbp
  __int64 v8; // rdi
  __int64 v9; // rax
  __int64 v10; // r15
  unsigned __int64 v11; // r15
  unsigned __int8 v12; // r14
  __int64 v13; // rcx
  __int64 v14; // r13
  __int64 v15; // r12
  unsigned int v16; // ebx
  __int64 v17; // rax
  __int64 v18; // r9
  unsigned int v19; // eax
  char v20; // cl
  __int64 v21; // rbx
  unsigned int v22; // eax
  char v23; // r8
  __int64 v24; // kr08_8
  __int64 v25; // kr18_8
  __int64 v26; // kr20_8
  __int64 v27; // rcx
  int v28; // ecx
  unsigned __int8 v29; // dl
  unsigned __int8 v30; // dl
  char v31; // kr02_1
  __int64 v32; // r8
  __int64 *v33; // rax
  unsigned int v34; // ebp
  __int64 *v35; // rax
  __int64 v36; // rax
  int v37; // eax
  __int64 v38; // rax
  __int64 v40; // rax
  __int64 v41; // rdx
  unsigned __int64 v42; // rdx
  __int64 v43; // rcx
  __int64 v44; // rdx
  __int64 v45; // rax
  __int64 v46; // rsi
  int v47; // ebx
  int v48; // ebp
  int v49; // eax
  unsigned __int8 v50; // [rsp+3Eh] [rbp-5Ah]
  char v52; // [rsp+40h] [rbp-58h]
  unsigned int v53; // [rsp+48h] [rbp-50h]

  v7 = a6;
  v8 = a5;
  v50 = a2;
  v53 = (char)a2;
  while ( 1 )
  {
    v52 = -1;
    if ( v50 != 0 )
    {
      switch ( v53 )
      {
        case '$':
        case '%':
        case '+':
          break;
        default:
          v52 = v53 - 9;
          break;
      }
    }
    v9 = a1[3];
    v10 = a1[4] - v9;
    if ( v10 != 0 )
    {
      v11 = v10 >> 3;
      v12 = v52 - 10;
      v13 = 1;
      if ( v11 < 2 )
        v11 = 1;
      if ( (a4 & 1) != 0 )
      {
        v14 = 0;
        while ( 1 )
        {
          v15 = *(_QWORD *)(a1[3] + 8 * v14);
          if ( (v8 & 1) != 0 || (*(_BYTE *)(v15 + 176) & 1) == 0 )
          {
            if ( *(_BYTE *)(v15 + 40) == v50 )
              return v15;
            if ( (*(__int64 (__fastcall **)(_QWORD *))(*a1 + 416LL))(a1) != 0 )
            {
              v16 = *(unsigned __int8 *)(v15 + 40);
              v17 = (*(__int64 (__fastcall **)(_QWORD *))(*a1 + 416LL))(a1);
              LOBYTE(v18) = 1;
              if ( (unsigned __int8)sub_140CC6A10(v17, v16, v50, v18) != 0 )
                return v15;
            }
            if ( v12 <= 0x14u )
            {
              v19 = *(char *)(v15 + 40);
              a2 = v19 - 9;
              v20 = 23;
              switch ( *(_BYTE *)(v15 + 40) )
              {
                case 9:
                case 0x2B:
                  goto LABEL_29;
                case 0xA:
                case 0x15:
                  if ( v52 != 21 )
                    goto LABEL_32;
                  goto LABEL_30;
                case 0xB:
                case 0x24:
                  if ( v52 != 19 )
                    goto LABEL_32;
                  goto LABEL_30;
                case 0xC:
                case 0x25:
                  if ( v52 != 18 )
                    goto LABEL_32;
                  goto LABEL_30;
                case 0x12:
                  if ( v52 != 20 )
                    goto LABEL_32;
                  goto LABEL_30;
                case 0x1D:
                  v20 = 17;
LABEL_29:
                  if ( v52 == v20 )
                    goto LABEL_30;
                  goto LABEL_32;
                case 0x21:
                  if ( v52 != 22 )
                    goto LABEL_32;
                  goto LABEL_30;
                default:
                  if ( v52 == 100 )
                  {
LABEL_30:
                    if ( v19 > 0x2B )
                      return v15;
                    a2 = 0x83000000000LL;
                    if ( !_bittest64(&a2, v19) )
                      return v15;
                  }
LABEL_32:
                  if ( ((unsigned __int8)v7 & ((_BYTE)v19 == 0)) == 1 && (unsigned __int8)sub_1411CC0E0(v15, a2) == v52 )
                    return v15;
                  break;
              }
            }
          }
          if ( v11 == ++v14 )
            goto LABEL_66;
        }
      }
      if ( v12 > 0x14u )
      {
        v27 = 0;
        if ( (v8 & 1) != 0 )
        {
          while ( 1 )
          {
            v15 = *(_QWORD *)(v9 + 8 * v27);
            LOBYTE(a2) = v50;
            if ( *(_BYTE *)(v15 + 40) == v50 )
              break;
            if ( v11 == ++v27 )
              goto LABEL_66;
          }
        }
        else
        {
          while ( 1 )
          {
            v15 = *(_QWORD *)(v9 + 8 * v27);
            if ( (*(_BYTE *)(v15 + 176) & 1) == 0 )
            {
              LOBYTE(a2) = v50;
              if ( *(_BYTE *)(v15 + 40) == v50 )
                break;
            }
            if ( v11 == ++v27 )
              goto LABEL_66;
          }
        }
      }
      else
      {
        v21 = 0;
        while ( 1 )
        {
          v15 = *(_QWORD *)(a1[3] + 8 * v21);
          if ( (v8 & 1) != 0 || (*(_BYTE *)(v15 + 176) & 1) == 0 )
            break;
LABEL_39:
          if ( v11 == ++v21 )
            goto LABEL_66;
        }
        v22 = *(char *)(v15 + 40);
        if ( *(_BYTE *)(v15 + 40) != v50 )
        {
          a2 = v22 - 9;
          v24 = v8;
          v25 = v7;
          v26 = v13;
          v23 = 23;
          v13 = (unsigned int)v8;
          v7 = (unsigned int)v7;
          v8 = (unsigned int)v8;
          switch ( *(_BYTE *)(v15 + 40) )
          {
            case 9:
            case 0x2B:
              goto LABEL_55;
            case 0xA:
            case 0x15:
              if ( v52 != 21 )
                goto LABEL_58;
              goto LABEL_56;
            case 0xB:
            case 0x24:
              if ( v52 != 19 )
                goto LABEL_58;
              goto LABEL_56;
            case 0xC:
            case 0x25:
              if ( v52 != 18 )
                goto LABEL_58;
              goto LABEL_56;
            case 0x12:
              if ( v52 != 20 )
                goto LABEL_58;
              goto LABEL_56;
            case 0x1D:
              v23 = 17;
LABEL_55:
              if ( v52 == v23 )
                goto LABEL_56;
              goto LABEL_58;
            case 0x21:
              if ( v52 != 22 )
                goto LABEL_58;
              goto LABEL_56;
            default:
              v13 = v26;
              v7 = v25;
              v8 = v24;
              if ( v52 == 100 )
              {
LABEL_56:
                if ( v22 > 0x2B )
                  return v15;
                v13 = v22;
                a2 = 0x83000000000LL;
                if ( !_bittest64(&a2, v22) )
                  return v15;
              }
LABEL_58:
              if ( ((unsigned __int8)v7 & ((_BYTE)v22 == 0)) == 1 && (unsigned __int8)sub_1411CC0E0(v15, a2) == v52 )
                return v15;
              goto LABEL_39;
          }
        }
      }
      return v15;
    }
LABEL_66:
    if ( a3 == 6 )
      goto LABEL_125;
    if ( a3 == 3 )
      break;
    if ( a3 == 4 || a3 == 1 )
    {
      v15 = 0;
      switch ( v53 )
      {
        case 1u:
          if ( (*(unsigned int (__fastcall **)(_QWORD *))(*a1 + 56LL))(a1) != 3 )
            goto LABEL_105;
          v33 = (__int64 *)a1[35];
          break;
        case 9u:
        case 0xFu:
          v28 = (int)a1;
          v29 = 1;
          goto LABEL_101;
        case 0xAu:
          v28 = (int)a1;
          v29 = 14;
          goto LABEL_101;
        case 0xBu:
          v28 = (int)a1;
          v29 = 18;
          goto LABEL_101;
        case 0xCu:
          v28 = (int)a1;
          v29 = 36;
          goto LABEL_101;
        case 0xEu:
          v28 = (int)a1;
          v29 = 33;
          goto LABEL_101;
        case 0x12u:
          v28 = (int)a1;
          v29 = 10;
          goto LABEL_101;
        case 0x1Du:
          v28 = (int)a1;
          v29 = 37;
          goto LABEL_101;
        case 0x21u:
          v28 = (int)a1;
          v29 = 43;
          goto LABEL_101;
        case 0x24u:
          v28 = (int)a1;
          v29 = 11;
          goto LABEL_101;
        case 0x25u:
          v28 = (int)a1;
          v29 = 12;
          goto LABEL_101;
        case 0x2Bu:
          v28 = (int)a1;
          v29 = 9;
LABEL_101:
          v36 = sub_1411DC000(v28, v29, 1, 0, 1, 0);
LABEL_102:
          v15 = v36;
          goto LABEL_103;
        default:
LABEL_103:
          if ( a3 == 1 )
            return v15;
LABEL_104:
          a4 = 0;
          LOBYTE(v8) = 1;
          a3 = 2;
          goto LABEL_120;
      }
      while ( 1 )
      {
        if ( v33 == (__int64 *)a1[36] )
          goto LABEL_122;
        a2 = *v33;
        if ( *(_QWORD **)(*v33 + 8) == a1 )
        {
          v34 = *(unsigned __int8 *)(a2 + 48);
          if ( v34 <= 0x14 )
          {
            v8 = 1049072;
            if ( _bittest((const int *)&v8, v34) )
              break;
          }
        }
        ++v33;
      }
      if ( *(_QWORD *)a2 == 0 )
      {
LABEL_122:
        v36 = sub_140E69670((__int64)a1, 1, v32);
        goto LABEL_102;
      }
      v35 = (__int64 *)a1[3];
      if ( v35 == (__int64 *)a1[4] )
      {
LABEL_105:
        v15 = 0;
        if ( a3 != 1 )
          goto LABEL_104;
      }
      else
      {
        v15 = *v35;
        if ( a3 != 1 )
          goto LABEL_104;
      }
      return v15;
    }
    if ( a3 != 5 && a3 != 2 )
      return 0;
    v15 = 0;
    v31 = a2;
    v30 = 29;
    switch ( v53 )
    {
      case 1u:
        v30 = 9;
        goto LABEL_117;
      case 9u:
        v30 = 43;
        goto LABEL_117;
      case 0xAu:
        v30 = 18;
        goto LABEL_117;
      case 0xBu:
        v30 = 36;
        goto LABEL_117;
      case 0xCu:
        v30 = 37;
        goto LABEL_117;
      case 0xEu:
        v30 = 10;
        goto LABEL_117;
      case 0xFu:
        v30 = 1;
        goto LABEL_117;
      case 0x12u:
        v30 = 11;
        goto LABEL_117;
      case 0x21u:
        v30 = 14;
        goto LABEL_117;
      case 0x24u:
        v30 = 12;
        goto LABEL_117;
      case 0x25u:
        goto LABEL_117;
      case 0x2Bu:
        v30 = 33;
LABEL_117:
        v15 = sub_1411DC000((_DWORD)a1, v30, 2, 0, 1, 0);
        break;
      default:
        LOBYTE(a2) = v31;
        break;
    }
    if ( a3 != 2 )
    {
      a4 = 0;
      a3 = 1;
      LOBYTE(v8) = 1;
LABEL_120:
      v7 = 0;
      if ( v15 == 0 )
        continue;
    }
    return v15;
  }
  if ( v53 > 0x1E || (v37 = 1073995784, !_bittest(&v37, v53)) )
  {
    if ( v50 != 9 )
    {
LABEL_137:
      v15 = sub_1411DC000((_DWORD)a1, v50, 1, 0, 1, 0);
      v45 = sub_1411DC000((_DWORD)a1, v50, 2, 0, 1, 0);
      if ( v45 != 0 )
      {
        v46 = v45;
        if ( v15 != 0 )
        {
          v47 = sub_1409B4B30(*(unsigned __int8 *)(v15 + 40));
          v48 = sub_1409B4B30(*(unsigned __int8 *)(v46 + 40));
          v49 = sub_1409B4B30(v50);
          if ( v49 - v47 >= v48 - v49 )
            return v46;
        }
        else
        {
          return v45;
        }
      }
      return v15;
    }
  }
LABEL_125:
  v38 = a1[6];
  if ( a1[7] != v38 )
    return *(_QWORD *)v38;
  v40 = a1[3];
  v41 = a1[4] - v40;
  if ( v41 == 0 )
    goto LABEL_137;
  v42 = v41 >> 3;
  v43 = 1;
  if ( v42 >= 2 )
    v43 = v42;
  v44 = 0;
  while ( 1 )
  {
    v15 = *(_QWORD *)(v40 + 8 * v44);
    if ( *(_BYTE *)(v15 + 40) == 3 )
      return v15;
    if ( v43 == ++v44 )
      goto LABEL_137;
  }
}
