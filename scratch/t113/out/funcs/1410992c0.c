__int64 __fastcall sub_1410992C0(char a1)
{
  __int64 v1; // rsi
  __int64 v2; // rsi
  __int64 v3; // rax
  __int64 v4; // rax
  __int64 v5; // rsi
  __int64 v6; // rsi
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 v9; // rax
  __int64 v10; // rax
  __int64 v11; // rsi
  __int64 v12; // rsi

  v1 = 0;
  switch ( a1 )
  {
    case 1:
      if ( dword_141B5CC70 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5CC70);
        if ( dword_141B5CC70 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B5CC20, 1100132798, 1024, 616, 0, 0, 1024, 4096);
          sub_141751048(sub_140DD7940);
          sub_141750EA0(&dword_141B5CC70);
        }
      }
      v2 = sub_1407E58C0(&unk_141B5CC20, 616);
      *(_QWORD *)(v2 + 8) = 0x141876F7CLL;
      *(_QWORD *)(v2 + 296) = 0x141876F88LL;
      *(_QWORD *)(v2 + 256) = -1;
      *(_DWORD *)(v2 + 264) = 0;
      *(_QWORD *)(v2 + 248) = 0x141889DA8LL;
      *(_QWORD *)(v2 + 272) = 0;
      sub_140DD7950(v2 + 288, 0);
      *(_QWORD *)v2 = 0x141876F98LL;
      *(_QWORD *)(*(int *)(*(_QWORD *)(v2 + 8) + 8LL) + v2 + 8) = 0x141876FB8LL;
      *(_QWORD *)(*(int *)(*(_QWORD *)(v2 + 8) + 4LL) + v2 + 8) = 0x141877008LL;
      v3 = *(int *)(*(_QWORD *)(v2 + 8) + 4LL);
      *(_DWORD *)(v3 + v2 + 4) = v3 - 240;
      v4 = *(int *)(*(_QWORD *)(v2 + 8) + 8LL);
      *(_DWORD *)(v4 + v2 + 4) = v4 - 280;
      *(_DWORD *)(v2 + 72) = 0;
      *(_QWORD *)(v2 + 64) = 0;
      *(_QWORD *)(v2 + 56) = 0;
      *(_QWORD *)(v2 + 48) = 0;
      *(_QWORD *)(v2 + 40) = 0;
      *(_QWORD *)(v2 + 32) = 0;
      *(_QWORD *)(v2 + 24) = 0;
      *(_QWORD *)(v2 + 16) = 0x141877808LL;
      *(_QWORD *)(v2 + 80) = 0;
      *(_QWORD *)(v2 + 88) = 0;
      *(_QWORD *)(v2 + 96) = 0;
      *(_QWORD *)(v2 + 104) = 0;
      *(_QWORD *)(v2 + 112) = 0;
      *(_QWORD *)(v2 + 120) = 0;
      *(_QWORD *)(v2 + 128) = 0;
      *(_QWORD *)(v2 + 136) = 0;
      *(_QWORD *)(v2 + 144) = 0;
      *(_QWORD *)(v2 + 152) = 0;
      *(_QWORD *)(v2 + 160) = 0;
      *(_QWORD *)(v2 + 168) = 0;
      *(_QWORD *)(v2 + 176) = 0;
      *(_QWORD *)(v2 + 184) = 0xFFFFFFFFLL;
      *(_QWORD *)(v2 + 192) = 0x76C0001076C0001LL;
      *(_QWORD *)(v2 + 200) = 124518401;
      *(_WORD *)(v2 + 223) = -256;
      *(_WORD *)(v2 + 216) = 0;
      *(_QWORD *)(v2 + 208) = 0;
      *(_QWORD *)(v2 + 226) = 0x303030302000000LL;
      *(_WORD *)(v2 + 234) = 771;
      *(_BYTE *)(v2 + 225) = 0;
      *(_DWORD *)(v2 + 218) = 0;
      *(_BYTE *)(v2 + 222) = 0;
      return v2 + *(int *)(*(_QWORD *)(v2 + 8) + 4LL) + 8;
    case 2:
      if ( dword_141B5D660 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5D660);
        if ( dword_141B5D660 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B5D610, 1100132874, 1024, 1000, 0, 0, 1024, 4096);
          sub_141751048(sub_140E44A30);
          sub_141750EA0(&dword_141B5D660);
        }
      }
      v2 = sub_1407E58C0(&unk_141B5D610, 1000);
      sub_140E06100(v2, 1);
      return v2 + *(int *)(*(_QWORD *)(v2 + 8) + 4LL) + 8;
    case 3:
      if ( dword_141B61560 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B61560);
        if ( dword_141B61560 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B61510, 1100132816, 64, 1240, 0, 0, 64, 4096);
          sub_141751048(sub_1410B5940);
          sub_141750EA0(&dword_141B61560);
        }
      }
      v5 = sub_1407E58C0(&unk_141B61510, 1240);
      sub_1415D4E50(v5, 1);
      return v5 + 872;
    case 4:
      if ( dword_141B61668 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B61668);
        if ( dword_141B61668 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B61618, 1100147973, 512, 344, 0, 0, 512, 4096);
          sub_141751048(sub_1410B5950);
          sub_141750EA0(&dword_141B61668);
        }
      }
      v6 = sub_1407E58C0(&unk_141B61618, 344);
      sub_141585480(v6, 1);
      return v6 + 312;
    case 5:
      if ( dword_141B5F3E0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B5F3E0);
        if ( dword_141B5F3E0 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B5F390, 1100130726, 0x4000, 48, 0, 0, 1024, 4096);
          sub_141751048(sub_140FB3BA0);
          sub_141750EA0(&dword_141B5F3E0);
        }
      }
      v1 = sub_1407E58C0(&unk_141B5F390, 48);
      *(_QWORD *)(v1 + 8) = -1;
      *(_DWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 24) = 0;
      v7 = 0x14188A548LL;
      goto LABEL_23;
    case 6:
      if ( dword_141B61610 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B61610);
        if ( dword_141B61610 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B615C0, 1100125638, 32, 168, 0, 0, 32, 4096);
          sub_141751048(sub_1410B5960);
          sub_141750EA0(&dword_141B61610);
        }
      }
      v8 = sub_1407E58C0(&unk_141B615C0, 168);
      *(_QWORD *)(v8 + 8) = 0x1418C5D28LL;
      v1 = v8 + 136;
      *(_QWORD *)(v8 + 144) = -1;
      *(_DWORD *)(v8 + 152) = 0;
      *(_QWORD *)(v8 + 160) = 0;
      *(_QWORD *)(v8 + 16) = 0;
      *(_QWORD *)(v8 + 24) = 0x76C0001076C0001LL;
      *(_QWORD *)(v8 + 32) = 0;
      *(_QWORD *)(v8 + 40) = 0;
      *(_QWORD *)(v8 + 48) = 0;
      *(_QWORD *)(v8 + 56) = 0;
      *(_QWORD *)(v8 + 64) = 0;
      *(_QWORD *)(v8 + 72) = 0;
      *(_QWORD *)(v8 + 80) = 0xA0A0A0A0A0A0A0ALL;
      *(_BYTE *)(v8 + 106) = 0;
      *(_QWORD *)(v8 + 88) = 0;
      *(_QWORD *)(v8 + 96) = 0;
      *(_WORD *)(v8 + 107) = -250;
      *(_WORD *)(v8 + 104) = -1;
      *(_QWORD *)v8 = 0x1418C5D38LL;
      *(_QWORD *)(v8 + 136) = 0x1418C5D68LL;
      *(_DWORD *)(v8 + 132) = 0;
      *(_QWORD *)(v8 + 112) = 0;
      *(_DWORD *)(v8 + 120) = 168427777;
      return v1;
    case 7:
      if ( dword_141B61718 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B61718);
        if ( dword_141B61718 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B616C8, 1100132852, 1024, 80, 0, 0, 1024, 4096);
          sub_141751048(sub_1410B5E80);
          sub_141750EA0(&dword_141B61718);
        }
      }
      v9 = sub_1407E58C0(&unk_141B616C8, 80);
      *(_QWORD *)(v9 + 8) = 0x1418C18BCLL;
      v1 = v9 + 48;
      *(_QWORD *)(v9 + 56) = -1;
      *(_DWORD *)(v9 + 64) = 0;
      *(_QWORD *)(v9 + 72) = 0;
      *(_QWORD *)v9 = 0x1418C18D8LL;
      *(_QWORD *)(v9 + 48) = 0x1418C1DA8LL;
      *(_DWORD *)(v9 + 44) = 0;
      *(_DWORD *)(v9 + 24) = 124518401;
      *(_WORD *)(v9 + 28) = -1;
      *(_QWORD *)(v9 + 16) = 0xFFF0BD51FFFFFFFFuLL;
      *(_BYTE *)(v9 + 36) = 0;
      *(_DWORD *)(v9 + 30) = 0;
      *(_WORD *)(v9 + 34) = -156;
      return v1;
    case 8:
      if ( dword_141B616C0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B616C0);
        if ( dword_141B616C0 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B61670, 1100151060, 512, 168, 0, 0, 512, 4096);
          sub_141751048(sub_1410B5E90);
          sub_141750EA0(&dword_141B616C0);
        }
      }
      v10 = sub_1407E58C0(&unk_141B61670, 168);
      *(_QWORD *)(v10 + 8) = 0x1418C5D28LL;
      v1 = v10 + 136;
      *(_QWORD *)(v10 + 144) = -1;
      *(_DWORD *)(v10 + 152) = 0;
      *(_QWORD *)(v10 + 160) = 0;
      *(_QWORD *)(v10 + 16) = 0;
      *(_QWORD *)(v10 + 24) = 0x76C0001076C0001LL;
      *(_QWORD *)(v10 + 32) = 0;
      *(_QWORD *)(v10 + 40) = 0;
      *(_QWORD *)(v10 + 48) = 0;
      *(_QWORD *)(v10 + 56) = 0;
      *(_QWORD *)(v10 + 64) = 0;
      *(_QWORD *)(v10 + 72) = 0;
      *(_QWORD *)(v10 + 80) = 0xA0A0A0A0A0A0A0ALL;
      *(_BYTE *)(v10 + 106) = 0;
      *(_QWORD *)(v10 + 88) = 0;
      *(_QWORD *)(v10 + 96) = 0;
      *(_WORD *)(v10 + 107) = -250;
      *(_WORD *)(v10 + 104) = -1;
      *(_QWORD *)v10 = 0x1418C6598LL;
      *(_QWORD *)(v10 + 136) = 0x1418C65C8LL;
      *(_DWORD *)(v10 + 132) = 0;
      *(_QWORD *)(v10 + 112) = 0;
      *(_WORD *)(v10 + 120) = 0;
      return v1;
    case 9:
      if ( dword_141B60E80 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B60E80);
        if ( dword_141B60E80 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B60E30, 1100132774, 1, 1472, 0, 0, 1, 4096);
          sub_141751048(sub_141032670);
          sub_141750EA0(&dword_141B60E80);
        }
      }
      v11 = sub_1407E58C0(&unk_141B60E30, 1472);
      sub_1410050F0(v11, 1);
      return v11 + 1104;
    case 16:
      if ( dword_141B614B0 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B614B0);
        if ( dword_141B614B0 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B61460, 1100129813, 1024, 48, 0, 0, 1024, 4096);
          sub_141751048(sub_1410B5930);
          sub_141750EA0(&dword_141B614B0);
        }
      }
      v1 = sub_1407E58C0(&unk_141B61460, 48);
      *(_QWORD *)(v1 + 8) = -1;
      *(_DWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 24) = 0;
      v7 = 0x14188ADA8LL;
LABEL_23:
      *(_QWORD *)v1 = v7;
      *(_QWORD *)(v1 + 32) = 0;
      *(_QWORD *)(v1 + 40) = 0;
      break;
    case 17:
      if ( dword_141ABE1F8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141ABE1F8);
        if ( dword_141ABE1F8 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141ABE1A8, 1100139768, 25000, 112, 0, 1, 10000, 4096);
          sub_141751048(sub_140E53F00);
          sub_141750EA0(&dword_141ABE1F8);
        }
      }
      v1 = sub_1407E58C0(&unk_141ABE1A8, 112);
      *(_QWORD *)(v1 + 8) = -1;
      *(_DWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 24) = 0;
      *(_QWORD *)v1 = 0x14187BD28LL;
      *(_QWORD *)(v1 + 32) = 0;
      *(_QWORD *)(v1 + 40) = 0;
      *(_QWORD *)(v1 + 48) = 0;
      *(_QWORD *)(v1 + 56) = 0;
      *(_QWORD *)(v1 + 64) = -1;
      *(_WORD *)(v1 + 92) = 0;
      *(_DWORD *)(v1 + 100) = 512;
      *(_BYTE *)(v1 + 104) = 0;
      *(_QWORD *)(v1 + 72) = 0;
      *(_QWORD *)(v1 + 80) = 0;
      *(_DWORD *)(v1 + 88) = 124518400;
      *(_DWORD *)(v1 + 94) = 0;
      *(_WORD *)(v1 + 98) = 0;
      break;
    case 18:
      if ( dword_141B615B8 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B615B8);
        if ( dword_141B615B8 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B61568, 1100127630, 64, 224, 0, 0, 64, 4096);
          sub_141751048(sub_1410B5B40);
          sub_141750EA0(&dword_141B615B8);
        }
      }
      v12 = sub_1407E58C0(&unk_141B61568, 224);
      sub_141434F00(v12, 1);
      v1 = v12 + 192;
      break;
    case 19:
      if ( dword_141B61508 > *(_DWORD *)(*((_QWORD *)NtCurrentTeb()->ThreadLocalStoragePointer + (unsigned int)TlsIndex)
                                       + 4LL) )
      {
        sub_141750E08(&dword_141B61508);
        if ( dword_141B61508 == -1 )
        {
          sub_1407E53D0((unsigned int)&unk_141B614B8, 1100153127, 1024, 56, 0, 0, 1024, 4096);
          sub_141751048(sub_1410B5CE0);
          sub_141750EA0(&dword_141B61508);
        }
      }
      v1 = sub_1407E58C0(&unk_141B614B8, 56);
      *(_QWORD *)(v1 + 8) = -1;
      *(_DWORD *)(v1 + 16) = 0;
      *(_QWORD *)(v1 + 24) = 0;
      *(_QWORD *)(v1 + 32) = 0;
      *(_QWORD *)(v1 + 40) = 0;
      *(_QWORD *)v1 = 0x14188B5B8LL;
      *(_DWORD *)(v1 + 48) = -1;
      break;
    default:
      return v1;
  }
  return v1;
}
