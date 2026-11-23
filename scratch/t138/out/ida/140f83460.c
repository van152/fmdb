__int64 __fastcall sub_140F83460(_QWORD *a1, _QWORD *a2)
{
  __int64 v4; // rbx
  __int64 v5; // r8
  _DWORD *v7; // rdi
  char v8; // [rsp+2Bh] [rbp-1Dh] BYREF
  unsigned int v9[7]; // [rsp+2Ch] [rbp-1Ch] BYREF

  v4 = *a2;
  (*(void (__fastcall **)(_QWORD, char *, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: &v8, a3: 1);
  if ( *(_DWORD *)(v4 + 16) != 0 )
  {
    LODWORD(v4) = 0;
  }
  else if ( v8 == -1 )
  {
    *a1 = 0;
    LOBYTE(v4) = 1;
  }
  else
  {
    LODWORD(v4) = 0;
    switch ( v8 )
    {
      case 0:
        LODWORD(v4) = sub_140F91B50(a1, a2, a3: qword_141B5FDA8, a4: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 1:
        LODWORD(v4) = sub_140F83A50(a1, a2);
        break;
      case 2:
        LODWORD(v4) = sub_140F92260(a1, a2, a3: qword_141B5FDB0, a4: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 3:
        LODWORD(v4) = sub_140F925B0(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FDB8,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 5:
        LODWORD(v4) = sub_140F92AB0(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FDC8,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 6:
        LODWORD(v4) = sub_140F91ED0(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FDE8,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 7:
        LODWORD(v4) = sub_140F81270(a1, a2, a3: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 8:
        LODWORD(v4) = sub_140F931C0(a1, a2, a3: qword_141B5FDF8, a4: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 9:
        LODWORD(v4) = sub_140F938D0(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FE08,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 10:
        LODWORD(v4) = sub_140F92E30(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FDD0,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 19:
        LODWORD(v4) = sub_140F931C0(a1, a2, a3: qword_141B5FE20, a4: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 21:
        LODWORD(v4) = sub_140F83E20(a1, a2, a3: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 23:
        LODWORD(v4) = sub_140F93C60(
                        a1: (unsigned int)&qword_141B5FDA8,
                        a2: (_DWORD)a1,
                        a3: (_DWORD)a2,
                        a4: qword_141B5FE38,
                        a5: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 24:
        LOBYTE(v5) = 4 - (byte_141B5FC2C == 0);
        LODWORD(v4) = sub_140F80980(a1, a2, a3: v5);
        break;
      case 25:
        LODWORD(v4) = sub_140F80B80(a1, a2, a3: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 28:
        if ( (_BYTE)word_141B60320 != 0 )
        {
          LODWORD(v4) = sub_140F842D0(a1, a2);
        }
        else
        {
          v9[0] = -1;
          v7 = (_DWORD *)*a2;
          (*(void (__fastcall **)(_DWORD *, unsigned int *, __int64))(*(_QWORD *)v7 + 40LL))(a1: v7, a2: v9, a3: 4);
          LOBYTE(v4) = v7[4] == 0;
          if ( v7[4] == 0 )
            *a1 = sub_140F45DB0(a1: qword_141B5FDB8, a2: v9[0]);
        }
        break;
      case 56:
        LODWORD(v4) = sub_140F91B50(a1, a2, a3: qword_141B5FE60, a4: (unsigned __int8)byte_141B5FC2C ^ 1u);
        break;
      case 57:
        LODWORD(v4) = sub_140F83870(a1, a2);
        break;
      default:
        return (unsigned int)v4;
    }
  }
  return (unsigned int)v4;
}
